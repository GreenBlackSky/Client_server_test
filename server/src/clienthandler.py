"""Module contains ClientHandler class."""

from socketserver import BaseRequestHandler
from pickle import dumps, loads
from command import Command
# from item import Item
# from account import Account


class ClientHandler(BaseRequestHandler):
    """Class produces ClientHandlers.

    ClientHandler provides client with information and executs queries.
    """

    _items = None
    _users = None

    @staticmethod
    def set_db(items_db, users_db):
        """Set data bases.

        If data bases are not set, exception will rise on connection attempt.
        """
        ClientHandler._items = items_db
        ClientHandler._users = users_db

    def __init__(self, *args):
        """Create handler.

        Overridden to check if data bases are set.
        """
        if self._items is None or self._users is None:
            raise Exception("Try create ClientHandler without databases.")
        super().__init__(*args)

    def handle(self):
        """Handle new connection."""
        print("New connection:", self.client_address)
        data = 'dummy'
        account = None
        while len(data):
            request = self.request.recv(1024)
            request = loads(request)
            self._process_request(request.command, request.data)
        print("Connection lost:", self.client_address)
        self.request.close()

    def _process_request(self, command, data):
        pass
