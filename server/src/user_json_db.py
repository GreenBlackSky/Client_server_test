"""Module contains UsersDB class.

It is used to read json-based data bases with User.
"""

from json import load, dump
from user import User


class UsersDB:
    """Class handles JSON-based data base with users."""

    def __init__(self, path):
        """Open connection with data base with users.

        Behaves like dict for the most part.
        Create new user if no user under given name is exists.
        """
        self._users = dict()
        self._path = path
        with open(path, "r") as stream:
            users = load(stream)
            for user_conf in users:
                user = User(user_conf["name"])
                user.credits = user_conf["credits"]
                for item in user_conf["items"]:
                    user.items[item] = user_conf["items"][item]
                self._users[user.name] = user

    def __contains__(self, user_name):
        """Check if db contains user with given name."""
        return (user_name in self._users)

    def create_user(self, user_name):
        """Create new user."""
        self._users[user_name] = User(user_name)

    def __getitem__(self, user_name):
        """Get user with given name."""
        if user_name not in self._users:
            raise KeyError
        return self._users[user_name]

    def keys(self):
        """Get all users names in data base as a list."""
        return list(self._users.keys())

    def values(self):
        """Get list of all users in data base."""
        return list(self._users.values())

    def commit(self):
        """Commit changes into data base."""
        db = list()
        for user in self._users.values():
            user_data = {
                "name": user.name,
                "credits": user.credits,
                "items": user.items
            }
            db.append(user_data)

        with open(self._path, "w") as stream:
            dump(db, stream)

# TODO OOP-style load and commit
