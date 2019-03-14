"""Module with some stuff required by both server and client."""

from enum import Enum, auto


class Request:
    """Request, which is used to pass info from client to server."""

    class Type(Enum):
        """Enum, which contains commands."""

        PING = auto()
        USER_EXISTS = auto()
        LOG_IN = auto()
        GET_NAME = auto()
        GET_CREDITS = auto()
        GET_MY_ITEMS = auto()
        GET_ALL_ITEMS = auto()
        PURCHASE_ITEM = auto()
        SELL_ITEM = auto()
        LOG_OUT = auto()

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


class Answer(Request):
    """Answer, that is used to pass info from server to client."""

    def __init__(self, request_type, success=True, data=None, message=None):
        """Create new answer."""
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
