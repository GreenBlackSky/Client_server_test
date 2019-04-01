"""Module with some stuff required by both server and client."""

from enum import Enum


class Request:
    """Request, which is used to pass info from client to server."""

    class Type(Enum):
        """Enum, which contains commands."""

        # users
        USER_EXISTS = 0
        GET_USER = 1
        GET_ALL_USERS = 2
        GET_ALL_USERS_NAMES = 3

        # items
        GET_ITEM = 4
        GET_ALL_ITEMS = 5
        GET_ALL_ITEMS_NAMES = 6

        # current user
        GET_CURRENT_USER = 7
        GET_CURRENT_USER_NAME = 8
        GET_CREDITS = 9

        # current user items
        USER_HAS = 10
        GET_USER_ITEMS = 11
        GET_USER_ITEMS_NAMES = 12

        # util
        PING = 13
        LOG_IN = 14
        PURCHASE_ITEM = 15
        SELL_ITEM = 16
        LOG_OUT = 17

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


class Response(Request):
    """Response, that is used to pass info from server to client."""

    def __init__(self, request_type, success=True, data=None, message=None):
        """Create new response."""
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
