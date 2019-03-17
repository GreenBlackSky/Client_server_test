"""Module contains ServerHandler."""

import socket
from pickle import dumps, loads
from request import Request


class ServerHandler:
    """ServerHandler handles connection with server on client side."""

    def __init__(self, host, port, timeout):
        """Initialize client.

        Later client will try to connect to given server,
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
        """Get responce from server.

        Raises an exception if connection lost.
        """
        return loads(self._socket.recv(1024))

    def execute(self, request_type, arg=None):
        """Send request and get responce from server.

        Raises an exception if connection lost.
        """
        self._send_request(request_type, arg)
        return self._get_responce()
