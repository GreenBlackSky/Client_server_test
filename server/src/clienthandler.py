"""Module contains ClientHandler."""

from socketserver import TCPServer, ThreadingMixIn, BaseRequestHandler
from pickle import dumps, loads

class ClientHandler(ThreadingMixIn, TCPServer):
    """ClientHandler handles connection with clients on server side."""

    class _Handler(BaseRequestHandler):

        server_fabric = None

        def setup(self):
            self.server_core = self.server_fabric.get_core()

        def handle(self):
            print("New connection:", self.client_address)
            while True:
                request = self.request.recv(1024)
                if not request:
                    break
                request = loads(request)
                responce = self.server_core.process_request(request)
                responce = dumps(responce)
                self.request.send(responce)
            print("Connection lost:", self.client_address)
            self.request.close()

    def __init__(self, port, server_fabric):
        """Initialize server, listening to given port.
        
        Takes port and server core fabric as arguments.
        """
        super().__init__(("127.0.0.1", port), ClientHandler._Handler)
        ClientHandler._Handler.server_fabric = server_fabric

    def exec(self):
        """Start an execution loop."""
        self.serve_forever()
