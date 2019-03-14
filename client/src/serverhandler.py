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
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._socket.settimeout(timeout)

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
        ret = True
        try:
            self._send_request(Request.Type.PING)
            self._get_responce()
        except:
            ret = False
        return ret

    def has_account(self, user_name):
        """Check if server has an account with given name."""
        connected = True
        answer = None
        try:
            self._send_request(Request.Type.USER_EXISTS, user_name)
            answer = self._get_responce()
        except:
            connected = False
        return answer.data, connected

    def get_name(self):
        """Request name of current user."""
        connected = True
        answer = None
        try:
            self._send_request(Request.Type.GET_NAME)
            answer = self._get_responce()
        except:
            connected = False
        if not connected:
            return None, connected
        if answer.success:
            return answer.data, connected
        else:
            return answer.message, connected

    def log_in(self, user_name):
        """Log in user."""
        connected = True
        try:
            self._send_request(Request.Type.LOG_IN, user_name)
            self._get_responce()
        except:
            connected = False
        return connected

    def get_credits(self):
        """Request number of credits on users account."""
        connected = True
        answer = None
        try:
            self._send_request(Request.Type.GET_CREDITS)
            answer = self._get_responce()
        except:
            connected = False
        if not connected:
            return None, connected
        if answer.success:
            return answer.data, connected
        else:
            return answer.message, connected

    def get_my_items(self):
        """Request items user have."""
        connected = True
        answer = None
        try:
            self._send_request(Request.Type.GET_MY_ITEMS)
            answer = self._get_responce()
        except:
            connected = False
        if not connected:
            return None, connected
        if answer.success:
            return answer.data, connected
        else:
            return answer.message, connected

    def get_all_items(self):
        """Request all acessible items."""
        connected = True
        answer = None
        try:
            self._send_request(Request.Type.GET_ALL_ITEMS)
            answer = self._get_responce()
        except:
            connected = False
        return answer.data, connected

    def log_out(self):
        """Log out user."""
        try:
            self._send_request(Request.Type.LOG_OUT, user_name)
            self._get_responce()
        except:
            pass

    def purchase_item(self, item):
        """Request buying item."""
        connected = True
        answer = None
        try:
            self._send_request(Request.Type.PURCHASE_ITEM, item)
            answer = self._get_responce()
        except:
            connected = False
        if not connected:
            return None, connected
        if answer.success:
            return answer.data, connected
        else:
            return answer.message, connected

    def sell_item(self, item):
        """Request selling item."""
        connected = True
        answer = None
        try:
            self._send_request(Request.Type.SELL_ITEM, item)
            answer = self._get_responce()
        except:
            connected = False
        if not connected:
            return None, connected
        if answer.success:
            return answer.data, connected
        else:
            return answer.message, connected

# TODO Pass exceptions to upper level
