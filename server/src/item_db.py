"""Module contains ItemsDB class.

It is used to read json-based data bases with Items.
"""

from json import load
from addshare import get_abs_path
from item import Item

def decode_item(data):
    """Method transform dict into Item.

    Take dict and if it has all necessary properties,
    return Item object.
    """
    if "name" in data and \
        "buy" in data and \
            "sell" in data:
        return Item(data["name"],
                    data["buy"],
                    data["sell"])

class ItemsDB:
    """Class handles JSON-based data base with items."""

    def __init__(self, path):
        """Open connection to data base with items."""
        self._items = dict()
        with open(get_abs_path() + path, "r") as stream:
            items = load(stream, object_hook=decode_item)
            self._items = {item.name: item for item in items}

    def values(self):
        """Get list of all items."""
        return list(self._items.values())

    def __contains__(self, item_name):
        """Check if item with given name is in db."""
        return (item_name in self._items)

    def __getitem__(self, item_name):
        """Get item with given name."""
        return self._items[item_name]
