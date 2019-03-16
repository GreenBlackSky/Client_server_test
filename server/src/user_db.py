"""Module contains UsersDB class.

It is used to read json-based data bases with User.
"""

from json import load, dump
from addshare import get_abs_path
from item import Item
from item_db import decode_item
from user import User

# def decode_user(data):
#     if "name" in data and \
#             "credits" in data and \
#                 "items" in data:
#         items = map(decode_item, data["items"])
#         ret = User(data["name"])
#         ret.credits = data["credits"]
#         ret.items.extend(items)
#         return ret


class UsersDB:
    """Class handles sqlite-based data base with users."""

    def __init__(self, path):
        """Open connection with data base with users."""
        self._users = dict()
        self._path = path
        with open(get_abs_path() + path, "r") as stream:
            # users = load(stream, object_hook=decode_user)
            # self._users = {user.name: user for user in users}
            users = load(stream)
            for user_conf in users:
                user = User(user_conf["name"])
                user.credits = user_conf["credits"]
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

    def check_and_add_user(self, user_name):
        """Add new user with given name to db.

        If user already exists, do nothing.
        """
        self._users[user_name] = self._users.get(user_name, User(user_name))

    def commit(self):
        """Commit changes into data base."""
        db = list()
        for user in self._users.values():
            user_data = {
                "name": user.name,
                "credits": user.credits,
                "items": list()
            }
            for item in user.items:
                item_data = {
                    "name": item.name,
                    "buy": item.buying_price,
                    "sell": item.selling_price
                }
                user_data["items"].append(item_data)
            db.append(user_data)

        with open(get_abs_path() + self._path, "w") as stream:
            dump(db, stream)
