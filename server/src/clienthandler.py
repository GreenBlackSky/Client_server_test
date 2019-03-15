"""Module contains ClientHandler."""

from socketserver import TCPServer, ThreadingMixIn, BaseRequestHandler
from pickle import dumps, loads


class ClientHandler(ThreadingMixIn, TCPServer):
    """NetworkServer handles connection with clients on server side."""

    class _Handler(BaseRequestHandler):

        server_core = None

        def handle(self):
            print("New connection:", self.client_address)
            data = 'dummy'
            while len(data):
                request = self.request.recv(1024)
                request = loads(request)
                answer = self.server_core.process_request(request)
                answer = dumps(answer)
                self.request.send(answer)
            print("Connection lost:", self.client_address)
            self.request.close()

    def __init__(self, port, server_core):
        """Initialize server, listening to given port."""
        super().__init__(("127.0.0.1", port), ClientHandler._Handler)
        ClientHandler._Handler.server_core = server_core

    def exec(self):
        """Start an execution loop."""
        self.serve_forever()
