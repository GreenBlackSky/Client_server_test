"""Module contains ClientHandler class."""

from socketserver import BaseRequestHandler


class ClientHandler(BaseRequestHandler):
    """Class produces ClientHandlers.

    ClientHandler provides client with information and executs queries.
    """

    _items = None
    _users = None

    @staticmethod
    def set_db(items_db, users_db):
        ClientHandler._items = items_db
        ClientHandler._users = users_db

    def __init__(self, *args):
        if self._items is None or self._users is None:
            raise Exception("Try create ClientHandler without databases.")
        super().__init__(*args)

    def handle(self):
        print("New connection:", self.client_address)
        data = 'dummy'
        while len(data):
            request = self.request.recv(1024).decode()
            self.request.send(bytes(request, "utf-8"))
        print("Connection lost:", self.client_address)
        self.request.close()
