"""Module contains NetworkClient."""

import socket
from netrequest import Request
from pickle import dumps, loads
from commands import Command


class NetworkClient:
    """NetworkClient handles connection with server on client side."""

    def __init__(self, server_ip, server_port, timeout):
        """Initialize client.

        On start client will try to connect to given server,
        on given port with given timeout(ms).
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._socket.settimeout(timeout)

    def _send_request(self, command, data=None):
        """Send request to server.

        Raises an exception if connection lost.
        """
        request = Request(command, data)
        self._socket.sendall(dumps(request))

    def _get_responce(self):
        """Get answer from server.

        Raises an exception if connection lost.
        """
        return loads(self._socket.recv(1024))

    def has_connection(self):
        """Check if client has connection with server."""
        ret = True
        try:
            self._send_request(Command.PING)
            self._get_responce()
        except:
            ret = False
        return ret

    def has_account(self, user_name):
        """Check if server has an account with given name."""
        connected = True
        ret = None
        try:
            self._send_request(Command.USER_EXISTS, user_name)
            ret = self._get_responce()
        except:
            connected = False
        return ret, connected

    def get_name(self):
        """Request name of current user."""
        connected = True
        ret = None
        try:
            self._send_request(Command.GET_NAME)
            ret = self._get_responce()
        except:
            connected = False
        return ret, connected

    def log_in(self, user_name):
        """Log in user."""
        connected = True
        try:
            self._send_request(Command.LOG_IN, user_name)
            self._get_responce()
        except:
            connected = False
        return connected

    def get_credits(self):
        """Request number of credits on users account."""
        connected = True
        ret = None
        try:
            self._send_request(Command.GET_CREDITS)
            ret = self._get_responce()
        except:
            connected = False
        return ret, connected

    def get_my_items(self):
        """Request items user have."""
        connected = True
        ret = None
        try:
            self._send_request(Command.GET_MY_ITEMS)
            ret = self._get_responce()
        except:
            connected = False
        return ret, connected
        # TODO what about if user is not logged in?

    def get_all_items(self):
        """Request all acessible items."""
        connected = True
        ret = None
        try:
            self._send_request(Command.GET_ALL_ITEMS)
            ret = self._get_responce()
        except:
            connected = False
        return ret, connected

    def log_out(self):
        """Log out user."""
        try:
            self._send_request(Command.LOG_IN, user_name)
            self._get_responce()
        except:
            pass
        # TODO make it moe like others

    def purchase_item(self, item):
        """Request buying item."""
        connected = True
        ret = None
        try:
            self._send_request(Command.PURCHASE_ITEM)
            ret = self._get_responce()
        except:
            connected = False
        return ret, connected

    def sell_item(self, item):
        """Request selling item."""
        connected = True
        ret = None
        try:
            self._send_request(Command.SELL_ITEM)
            ret = self._get_responce()
        except:
            connected = False
        return ret, connected

# TODO pass exceptions to upper level
