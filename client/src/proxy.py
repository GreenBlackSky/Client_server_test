
from request import Request, Responce

class Proxy:
    def __init__(self, server):
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
        self._server.reconnect()
        self._get_game_info()

    def execute(self, request_type, arg=None):
        if request_type in self._updaters:
            ret = self._server.execute(request_type, arg)
            if ret.success:
                self._updaters[request_type](arg)
            return ret
        elif self._cache.get(request_type, None):
            return Responce(request_type, data=self._cache[request_type])
        return self._server.execute(request_type, arg)        

    def _get_game_info(self, *_):
        self._cache[Request.Type.GET_ALL_USERS_NAMES] = \
            self._server.execute(Request.Type.GET_ALL_USERS_NAMES).data
        self._cache[Request.Type.GET_ALL_ITEMS] = \
            self._server.execute(Request.Type.GET_ALL_ITEMS).data

    def _get_user_info(self, *_):
        self._cache[Request.Type.GET_CURRENT_USER_NAME] = \
            self._server.execute(Request.Type.GET_CURRENT_USER_NAME).data
        self._cache[Request.Type.GET_CREDITS] = \
            self._server.execute(Request.Type.GET_CREDITS).data
        self._cache[Request.Type.GET_USER_ITEMS_NAMES] = \
            self._server.execute(Request.Type.GET_USER_ITEMS_NAMES).data

    def _clear_user_info(self, *_):
        for request_type in [
            Request.Type.GET_CURRENT_USER_NAME,
            Request.Type.GET_CREDITS,
            Request.Type.GET_USER_ITEMS_NAMES
        ]:
            self._cache[request_type] = None

    def _handle_purchase(self, item_name):
        self._get_user_info()

    def _handle_sale(self, item_name):
        self._get_user_info()

# TODO 3 modify local info on deal without full update
