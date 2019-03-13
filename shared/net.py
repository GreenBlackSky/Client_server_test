"""Module contains network logic."""

from socket import socket


class NetworkClient:
    """NetworkClient handles connection with server on client side."""

    def __init__(self, server_ip, server_port, attempts, timeout):
        """Initialize client.

        On start client will try to connect to given server,
        on given port, for given number of attempts with given timeout(ms).
        """
    pass

    def has_connection():
        pass

    def check_account(user_name):
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


class NetworkServer:
    """NetworkServer handles connection with clients on server side."""

    def __init__(self, port):
        """Initialize server, listening to given port."""
        pass
