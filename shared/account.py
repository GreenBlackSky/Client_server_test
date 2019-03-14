"""Module contains tools for working with user accounts."""

# import sqlite3


class Account:
    """Account contains information about user."""

    def __init__(self, name):
        """Create new account."""
        self._name = name
        self._credits = 0
        self._items = list()

    @property
    def name(self):
        """Get user name"""
        return self._name

    @property
    def credits(self):
        """Get number of credits user have."""
        return self._credits

    @credits.setter
    def credits(self, val):
        self._credits = val

    @property
    def items(self):
        """Get items user have."""
        return self._items


class UsersDB:
    """Class handles sqlite-based data base with users."""

    def __init__(self, path):
        """Open connection with data base with accounts."""
        self.dummy_users = dict()

# TODO implement __iter__
