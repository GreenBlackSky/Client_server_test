
from request import Request, Responce

class Proxy:
    def __init__(self, server):
        self._server = server
        self._cache = {
            Request.Type.GET_ALL_USERS: None,
            Request.Type.GET_ALL_ITEMS: None,
            Request.Type.GET_NAME: None,
            Request.Type.GET_CREDITS: None,
            Request.Type.GET_MY_ITEMS: None
        }
        self._updaters = {
            Request.Type.LOG_IN: self._get_user_info,
            Request.Type.LOG_OUT: self._clear_user_info,
            Request.Type.PURCHASE_ITEM: self._get_user_info,
            Request.Type.SELL_ITEM: self._get_user_info
        }

    def reconnect(self):
        self._server.reconnect()
        self._get_game_info()

    def execute(self, request_type, arg=None):
        if request_type in self._updaters:
            return self._handle_request(self._updaters[request_type],
                                        request_type, arg)
        elif self._cache.get(request_type, None):
            return Responce(request_type, data=self._cache[request_type])
        return self._server.execute(request_type, arg)

    def _handle_request(self, updater, request_type, arg):
        ret = self._server.execute(request_type, arg)
        if ret.success:
            updater()
        return ret

    def _get_game_info(self):
        self._cache[Request.Type.GET_ALL_USERS] = \
            self._server.execute(Request.Type.GET_ALL_USERS).data
        self._cache[Request.Type.GET_ALL_ITEMS] = \
            self._server.execute(Request.Type.GET_ALL_ITEMS).data

    def _get_user_info(self):
        self._cache[Request.Type.GET_NAME] = \
            self._server.execute(Request.Type.GET_NAME).data
        self._cache[Request.Type.GET_CREDITS] = \
            self._server.execute(Request.Type.GET_CREDITS).data
        self._cache[Request.Type.GET_MY_ITEMS] = \
            self._server.execute(Request.Type.GET_MY_ITEMS).data

    def _clear_user_info(self):
        for request_type in [
            Request.Type.GET_NAME,
            Request.Type.GET_CREDITS,
            Request.Type.GET_MY_ITEMS
        ]:
            self._cache[request_type] = None

# TODO modify local info on deal without full update
