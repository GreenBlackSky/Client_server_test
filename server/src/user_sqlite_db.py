"""Module contains UsersDB class.

It is used to read sqlite-based data bases with User.
"""

from sqlite3 import connect as connect_sqlite
from user import User


class UsersDB:
    """Class handles SQLite-based data base with users."""

    def __init__(self, path):
        """Open connection with data base with users.

        Behaves like dict for the most part.
        """
        self._path = path
        self._users = dict()

    def _execute(self, query, *args):
        with connect_sqlite(self._path) as connection:
            cursor = connection.cursor()
            cursor.execute(query, *args)
            ret = cursor.fetchall()
            return ret

    def __contains__(self, user_name):
        """Check if db contains user with given name."""
        tuples = self._execute(
            "SELECT name FROM users WHERE name == ?",
            (user_name,)
        )
        return len(tuples) == 1

    def create_user(self, user_name):
        """Create new user."""
        self._execute(
            "INSERT INTO users (name, credits) VALUES (?, ?)",
            (user_name, 0)
        )
        self._users[user_name] = User(user_name)

    def __getitem__(self, user_name):
        """Get user with given name.

        Also stores user in internal cache, use with caution.
        """
        if user_name in self._users:
            return self._users[user_name]

        tuples = self._execute(
            "SELECT name, credits FROM users WHERE name == ?",
            (user_name,)
        )
        if not tuples:
            raise KeyError

        user_name, user_credits = tuples[0]
        user = User(user_name)
        user.credits = user_credits
        tuples = self._execute(
            "SELECT item_name, amount \
             FROM users_items \
             WHERE user_name == ?",
            (user_name,)
        )
        for item_name, amount in tuples:
            user.items[item_name] = amount

        self._users[user_name] = user
        return user

    def keys(self):
        """Get all users names in data base as a list."""
        tuples = self._execute("SELECT name FROM users")
        ret = [tup[0] for tup in tuples]
        return ret

    def values(self):
        """Get list of all users in data base.

        Also stores users in internal cache, use with caution.
        """
        return [self[name] for name in self.keys()]

    def commit(self):
        """Commit changes into data base."""
        for user_name, user in self._users.items():
            self._execute(
                "UPDATE users \
                 SET credits = ? \
                 WHERE name == ?",
                (user.credits, user_name)
            )
            for item_name, amount in user.items.items():
                self._execute(
                    "REPLACE INTO users_items VALUES (?, ?, ?)",
                    (user_name, item_name, amount)
                )
