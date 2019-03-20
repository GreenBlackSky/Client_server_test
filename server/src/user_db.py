"""Module contains UsersDB class.

It is used to read json-based data bases with User.
"""

from json import load, dump
from addshare import get_abs_path
from item import Item
from item_db import decode_item
from user import User


class UsersDB:
    """Class handles JSON-based data base with users."""

    def __init__(self, path):
        """Open connection with data base with users."""
        self._users = dict()
        self._path = path
        with open(get_abs_path() + path, "r") as stream:
            users = load(stream)
            for user_conf in users:
                user = User(user_conf["name"])
                user.credits = user_conf["credits"]
                for item in user_conf["items"]:
                    user.items[item] = user.items.get(item, 0) + 1
                self._users[user.name] = user  

    def __contains__(self, user_name):
        """Check if db contains user with given name."""
        return (user_name in self._users)

    def __getitem__(self, user_name):
        """Get user with given name.
        
        If no user under such name exists, create one.
        """
        if user_name not in self._users:
            self._users[user_name] = User(user_name)
        return self._users[user_name]

    def keys(self):
        """Get all users names in data base as a list."""
        return list(self._users.keys())

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

        with open(get_abs_path() + self._path, "w") as stream:
            dump(db, stream)

# TODO OOP-style load and commit
