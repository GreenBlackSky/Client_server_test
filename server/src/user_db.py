"""Module contains UsersDB class.

It is used to read json-based data bases with User.
"""

from json import load
from addshare import get_abs_path
from item import Item
from user import User


class UsersDB:
    """Class handles sqlite-based data base with users."""

    def __init__(self, path):
        """Open connection with data base with users."""
        self._users = dict()
        with open(get_abs_path() + path, "r") as stream:
            users = load(stream)
            for user_conf in users:
                user = User(user_conf["name"])
                for item_conf in user_conf["items"]:
                    item = Item(item_conf["name"],
                                item_conf["buy"],
                                item_conf["sell"])
                    user.items.append(item)
                self._users[user.name] = user

    def __contains__(self, user_name):
        """Check if db contains user with given name."""
        return (user_name in self._users)

    def __getitem__(self, user_name):
        """Get user with given name."""
        return self._users[user_name]
