"""Module contains tools for working with user accounts."""

# import sqlite3


class Account:
    """Account contains information about user."""

    def __init__(self, name):
        """Create new account."""
        self.name = name
        self.credits = 0
        self.items = list()


class UsersDB:
    """Class handles sqlite-based data base with users."""

    def __init__(self, path):
        """Open connection with data base with accounts."""
        self.dummy_users = dict()
