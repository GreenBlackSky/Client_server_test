"""Module contains ClientHandler."""

from socketserver import TCPServer, ThreadingMixIn, BaseRequestHandler
from pickle import dumps, loads


class ClientHandler(ThreadingMixIn, TCPServer):
    """ClientHandler handles connection with clients on server side.

    TCP-based.
    """

    class _Handler(BaseRequestHandler):

        server_core = None

        def setup(self):
            self._server = self.server_core.get_handler()

        def handle(self):
            print("New connection:", self.client_address)
            while True:
                request = self.request.recv(1024)
                if not request:
                    break
                request = loads(request)
                response = self._server.process_request(request)
                response = dumps(response)
                self.request.send(response)
            print("Connection lost:", self.client_address)
            self.request.close()

        def finish(self):
            self._server.deactivate_user()

    def __init__(self, port, server_core):
        """Initialize server, listening to given port.

        Takes port and ServerCore instance as arguments.
        """
        super().__init__(("127.0.0.1", port), ClientHandler._Handler)
        ClientHandler._Handler.server_core = server_core
