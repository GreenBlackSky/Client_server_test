"""Module with some stuff required by both server and client."""

from enum import Enum


class Request:
    """Request, which is used to pass info from client to server."""

    class Type(Enum):
        """Enum, which contains commands."""

        PING = 0
        USER_EXISTS = 1
        LOG_IN = 2
        GET_NAME = 3
        GET_CREDITS = 4
        GET_MY_ITEMS = 5
        GET_ALL_ITEMS = 6
        PURCHASE_ITEM = 7
        SELL_ITEM = 8
        LOG_OUT = 9

    def __init__(self, request_type, data=None):
        """Create new request."""
        self._type, self._data = request_type, data

    @property
    def request_type(self):
        """Get type of request."""
        return self._type

    @property
    def data(self):
        """Get data."""
        return self._data


class Responce(Request):
    """Responce, that is used to pass info from server to client."""

    def __init__(self, request_type, success=True, data=None, message=None):
        """Create new responce."""
        super().__init__(request_type, data)
        self._success = success
        self._message = message

    @property
    def success(self):
        """Check if request was successfull."""
        return self._success

    @property
    def message(self):
        """Get additional info on request."""
        return self._message
