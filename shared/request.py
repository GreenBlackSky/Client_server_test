"""Module with some stuff required by both server and client."""

from enum import Enum


class Request:
    """Request, which is used to pass info from client to server."""

    class Type(Enum):
        """Enum, which contains commands."""

        PING = 0
        USER_EXISTS = 1
        GET_ALL_USERS_NAMES = 2
        LOG_IN = 3
        GET_CURRENT_USER_NAME = 4
        GET_CREDITS = 5
        GET_USER_ITEMS_NAMES = 6
        GET_ALL_ITEMS = 7
        PURCHASE_ITEM = 8
        SELL_ITEM = 9
        LOG_OUT = 10

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

# TODO 4 GET_USER and GET_ITEM
