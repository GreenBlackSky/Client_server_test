

class Proxy:
    def __init__(self, server):
        self._server = server

    def reconnect(self):
        self._server.reconnect()

    def execute(self, request_type, arg=None):
        return self._server.execute(request_type, arg)

# TODO load info about users on connect, market and user on login
