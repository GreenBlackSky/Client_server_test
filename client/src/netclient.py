"""Module contains NetworkClient."""

from socket import socket


class NetworkClient:
    """NetworkClient handles connection with server on client side."""

    def __init__(self, host, port, attempts, timeout):
        """Initialize client.

        On start client will try to connect to given server,
        on given port, for given number of attempts with given timeout(ms).
        """
        self.host, self.port = host, port
        self.attempts, self.timeout = attempts, timeout
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect()

    def _send_data(self, data):
        pass

    def _get_data(self):
        pass

    def has_connection():
        pass

    def has_account(user_name):
        pass

    def log_in(user_name):
        pass

    def get_credits():
        pass

    def get_my_items():
        pass

    def get_all_items():
        pass

    def log_out():
        pass

    def purchase_item(item):
        pass

    def sell_item(item):
        pass
