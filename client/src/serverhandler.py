"""Module contains NetworkClient."""

import socket
from pickle import dumps, loads
from netrequest import Request


class ServerHandler:
    """ServerHandler handles connection with server on client side."""

    def __init__(self, host, port, timeout):
        """Initialize client.

        On start client will try to connect to given server,
        on given port with given timeout(ms).
        """
        self._host, self._port = host, port
        self._socket = None
        self._timeout = timeout

    def reconnect(self):
        """Close connection if open, and try to connect again."""
        if self._socket:
            self._socket.close()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        self._socket.settimeout(self._timeout)

    def _send_request(self, request_type, data=None):
        """Send request to server.

        Raises an exception if connection lost.
        """
        request = Request(request_type, data)
        self._socket.sendall(dumps(request))

    def _get_responce(self):
        """Get answer from server.

        Raises an exception if connection lost.
        """
        answer = loads(self._socket.recv(1024))
        return answer

    def ping(self):
        """Check if client has connection with server."""
        self._send_request(Request.Type.PING)
        self._get_responce()

    def log_in(self, user_name):
        """Log in user."""
        self._send_request(Request.Type.LOG_IN, user_name)
        self._get_responce()

    def log_out(self):
        """Log out user."""
        self._send_request(Request.Type.LOG_OUT)
        self._get_responce()

# TODO everython below can be done in ONE method. But is it worth it?

    def has_user(self, user_name):
        """Check if server has an user with given name."""
        self._send_request(Request.Type.USER_EXISTS, user_name)
        answer = self._get_responce()
        return answer.data

    def get_name(self):
        """Request name of current user."""
        self._send_request(Request.Type.GET_NAME)
        answer = self._get_responce()
        if answer.success:
            return answer.data
        else:
            return answer.message

    def get_credits(self):
        """Request number of credits user have."""
        self._send_request(Request.Type.GET_CREDITS)
        answer = self._get_responce()
        if answer.success:
            return answer.data
        else:
            return answer.message

    def get_my_items(self):
        """Request items user have."""
        self._send_request(Request.Type.GET_MY_ITEMS)
        answer = self._get_responce()
        if answer.success:
            return answer.data
        else:
            return answer.message

    def get_all_items(self):
        """Request all acessible items."""
        self._send_request(Request.Type.GET_ALL_ITEMS)
        answer = self._get_responce()
        return answer.data

    def purchase_item(self, item):
        """Request buying item."""
        self._send_request(Request.Type.PURCHASE_ITEM, item)
        answer = self._get_responce()
        return (answer.data, answer.message)

    def sell_item(self, item):
        """Request selling item."""
        self._send_request(Request.Type.SELL_ITEM, item)
        answer = self._get_responce()
        return (answer.data, answer.message)
