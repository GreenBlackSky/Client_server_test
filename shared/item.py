"""Module contains class Item and ItemsDB."""

# import sqlite


class Item:
    """Item object contains item name and its price."""

    def __init__(self, name, buying_price, selling_price):
        """Create new item."""
        self._name = name
        self._buying_price = buying_price
        self._selling_price = selling_price

    @property
    def name(self):
        """Name of item."""
        return self._name

    @property
    def buying_price(self):
        """Get number of credits required to buy the item."""
        return self._buying_price

    @property
    def selling_price(self):
        """Get number of credits accired by selling the item."""
        return self._selling_price

    def __eq__(self, other):
        """Check if this item id identical with the other."""
        if (isinstance(other, Item) and
                self.name == other.name and
                self.buying_price == other.buying_price and
                self.selling_price == other.selling_price):
            return True
        return False

    def __repr__(self):
        """Represent item in string form.

        Contains new lines.
        """
        return "{}:\n\tbuy: {}\n\tsell: {}".format(
            self.name,
            self.buying_price,
            self.selling_price
        )


class ItemsDB:
    """Class handles sqlite-based data base with items."""

    def __init__(self, path):
        """Open connection to data base with items."""
        self.dummy_items = {
            "hat": Item("hat", 10, 5),
            "shirt": Item("shirt", 20, 10),
            "pants": Item("pants", 40, 20),
            "boots": Item("boots", 80, 40),
            "shovel": Item("shovel", 160, 80)
        }
