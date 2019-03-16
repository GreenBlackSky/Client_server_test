"""Module contains ItemsDB class.

It is used to read json-based data bases with Items.
"""

from json import load
from addshare import get_abs_path
from item import Item

def decode_item(data):
    if "name" in data and \
        "buy" in data and \
            "sell" in data:
        return Item(data["name"],
                    data["buy"],
                    data["sell"])


class ItemsDB:
    """Class handles sqlite-based data base with items."""

    def __init__(self, path):
        """Open connection to data base with items."""
        self._items = dict()
        with open(get_abs_path() + path, "r") as stream:
            items = load(stream, object_hook=decode_item)
            self._items = {item.name: item for item in items}

    @staticmethod
    def encode_item(item):
        if not isinstance(item, Item):
            type_name = z.__class__.__name__
            raise TypeError("{} is not JSON serializable".format(type_name))
        return {
            "type": "Item",
            "name": item.name,
            "buy": item.buying_price,
            "sell": item.selling_price
        }

    def values(self):
        """Get list of all items."""
        return list(self._items.values())

    def __contains__(self, item_name):
        """Check if item with given name is in db."""
        return (item_name in self._items)

    def __getitem__(self, item_name):
        """Get item with given name."""
        return self._items[item_name]
