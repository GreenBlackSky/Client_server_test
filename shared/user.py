"""Module contains class User."""


class User:
    """User contains information about user."""

    def __init__(self, name):
        """Create new user."""
        self._name = name
        self._credits = 0
        self._items = list()

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
        return self.name + "\n" + [str(item) + "\n" for item in self.items]
