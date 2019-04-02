"""Module contains ItemsDB class.

It is used to read sqlite-based data bases with Items.
"""

from sqlite3 import connect as connect_sqlite
from item import Item


class ItemsDB:
    """Class handles SQLite-based data base with items.

    Behaves like dict for the most part.
    """

    def __init__(self, path):
        """Open connection to data base with items."""
        self._path = path

    def _execute(self, query, *args):
        with connect_sqlite(self._path) as connection:
            cursor = connection.cursor()
            cursor.execute(query, *args)
            ret = cursor.fetchall()
            return ret

    def keys(self):
        """Get list of all items names in data base."""
        tuples = self._execute("SELECT name FROM items")
        ret = [tup[0] for tup in tuples]
        return ret

    def values(self):
        """Get list of all items."""
        tuples = self._execute(
            "SELECT name, selling_price, buying_price FROM items"
        )
        return [Item(name, buy, sell) for name, buy, sell in tuples]

    def __contains__(self, item_name):
        """Check if item with given name is in db."""
        tuples = self._execute(
            "SELECT name FROM items WHERE name == ?",
            (item_name,)
        )
        return len(tuples) == 1

    def __getitem__(self, item_name):
        """Get item with given name."""
        tuples = self._execute(
            "SELECT name, selling_price, buying_price \
             FROM items \
             WHERE name == ?",
            (item_name,)
        )
        if not tuples:
            raise KeyError
        name, buy, sell = tuples[0]
        return Item(name, buy, sell)

# TODO check about multythread access
