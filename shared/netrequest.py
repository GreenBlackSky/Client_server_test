"""Module with some stuff required by both server and client."""

from commands import Command


class Request:
    def __init__(self, command, data=None):
        self._command, self._data = command, data
