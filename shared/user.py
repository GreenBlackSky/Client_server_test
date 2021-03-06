"""Module contains class User."""


class User:
    """User contains information about user."""

    def __init__(self, name):
        """Create new user."""
        self._name = name
        self._credits = 0
        self._items = dict()

    @property
    def name(self):
        """Get user name."""
        return self._name

    @property
    def credits(self):
        """Get number of credits user have."""
        return self._credits

    @credits.setter
    def credits(self, val):
        self._credits = val

    @property
    def items(self):
        """Get items user have."""
        return self._items

    def __repr__(self):
        """Represent user in string form.

        Contains new lines.
        """
        ret = f"Name: {self.name}\nCredits: {self.credits}\nItems:\n"
        for item, quantity in self.items.items():
            ret.append(f"{item}: {quantity}\n")
        return ret
