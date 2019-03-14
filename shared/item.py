"""Module contains Item object."""


class Item:
    def __init__(self, name, buying_price, selling_price):
        self._name = name
        self._buying_price = buying_price
        self._selling_price = selling_price

    @property
    def name(self):
        return self._name

    @property
    def buying_price(self):
        return self._buying_price

    @property
    def selling_price(self):
        return self._selling_price

    def __eq__(self, other):
        if isinstance(other, Item) \
            and self.name == other.name \
                and self.buying_price == other.buying_price \
                    and self.selling_price == other.selling_price:
            return True
        return False

    def __repr__(self):
        return "{}:\n\tbuy: {}\n\tsell: {}".format(
            self.name,
            self.buying_price,
            self.selling_price
        )
