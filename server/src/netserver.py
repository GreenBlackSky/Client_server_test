"""Module contains NetworkServer."""

from socketserver import TCPServer, ThreadingMixIn


class NetworkServer(ThreadingMixIn, TCPServer):
    """NetworkServer handles connection with clients on server side."""

    def __init__(self, port, client_handler):
        """Initialize server, listening to given port."""
        super().__init__(("127.0.0.1", port), client_handler)

    def exec(self):
        """Start an execution loop."""
        self.serve_forever()
