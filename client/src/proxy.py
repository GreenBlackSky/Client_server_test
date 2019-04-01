"""Moduel contains Proxy class."""

from request import Request, Response


class Proxy:
    """Cache proxy.

    Proxy is created to decrease number of network communication
    between server and client.
    It wraps ServerHandler instance.
    Proxy has cache, which is updated when necessary.
    It is used to provide client with some info without asking server.
    """

    def __init__(self, server):
        """Create Proxy.

        Takes real ServerHandler as argument.
        """
        self._server = server
        self._cache = {
            Request.Type.GET_ALL_USERS_NAMES: None,
            Request.Type.GET_ALL_ITEMS: None,
            Request.Type.GET_CURRENT_USER_NAME: None,
            Request.Type.GET_CREDITS: None,
            Request.Type.GET_USER_ITEMS_NAMES: None
        }
        self._updaters = {
            Request.Type.LOG_IN: self._get_user_info,
            Request.Type.LOG_OUT: self._clear_user_info,
            Request.Type.PURCHASE_ITEM: self._handle_purchase,
            Request.Type.SELL_ITEM: self._handle_sale
        }

    def reconnect(self):
        """Wrapps ServerHandler.reconnect."""
        self._server.reconnect()
        self._get_game_info()

    def execute(self, request_type, arg=None):
        """Wrapps ServerHandler.execute.

        Update cache and use it to provide responses when possible.
        """
        if request_type in self._updaters:
            ret = self._server.execute(request_type, arg)
            if ret.success:
                self._updaters[request_type](arg)
        elif self._cache.get(request_type, None):
            ret = Response(request_type, data=self._cache[request_type])
        else:
            ret = self._server.execute(request_type, arg)
        return ret

    def _get_game_info(self, *_):
        self._cache[Request.Type.GET_ALL_USERS_NAMES] = \
            self._server.execute(Request.Type.GET_ALL_USERS_NAMES).data
        self._cache[Request.Type.GET_ALL_ITEMS] = \
            self._server.execute(Request.Type.GET_ALL_ITEMS).data

    def _get_user_info(self, *_):
        user = self._server.execute(Request.Type.GET_CURRENT_USER).data
        self._cache[Request.Type.GET_CURRENT_USER_NAME] = user.name
        self._cache[Request.Type.GET_CREDITS] = user.credits
        self._cache[Request.Type.GET_USER_ITEMS_NAMES] = user.items
        if user.name not in self._cache[Request.Type.GET_ALL_USERS_NAMES]:
            self._cache[Request.Type.GET_ALL_USERS_NAMES].append(user.name)

    def _clear_user_info(self, *_):
        for request_type in [
            Request.Type.GET_CURRENT_USER_NAME,
            Request.Type.GET_CREDITS,
            Request.Type.GET_USER_ITEMS_NAMES
        ]:
            self._cache[request_type] = None

    def _handle_purchase(self, item_name):
        item = self._server.execute(Request.Type.GET_ITEM, item_name).data
        self._cache[Request.Type.GET_CREDITS] -= item.buying_price
        self._cache[Request.Type.GET_USER_ITEMS_NAMES][item_name] = \
            self._cache[Request.Type.GET_USER_ITEMS_NAMES].get(item_name, 0) \
            + 1

    def _handle_sale(self, item_name):
        item = self._server.execute(Request.Type.GET_ITEM, item_name).data
        self._cache[Request.Type.GET_CREDITS] += item.selling_price
        self._cache[Request.Type.GET_USER_ITEMS_NAMES][item_name] -= 1
        if self._cache[Request.Type.GET_USER_ITEMS_NAMES][item_name] == 0:
            self._cache[Request.Type.GET_USER_ITEMS_NAMES].pop(item_name)

# TODO handle every request type
