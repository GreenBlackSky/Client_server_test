"""Module with some stuff required by both server and client."""

from commands import Command


class Request:
    """Request, which is used to pass info from client to server."""

    def __init__(self, command, data=None):
        """Create new request."""
        self._command, self._data = command, data
