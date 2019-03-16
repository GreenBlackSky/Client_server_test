"""Module contains ServerFabric class."""

from servercore import ServerCore


class ServerFabric:
    """Instances of ServerFabric generates ServerCore objects.

    Generated objects has properties,
    passed to ServerFabric itself.
    """
    def __init__(self, items_db, users_db,
                       min_limit, max_limit,
                       save_frequency):
        """Create ServerFabric."""
        self._items = items_db
        self._users = users_db
        self._new_credits_max = max_limit
        self._new_credits_min = min_limit
        self._save_frequency = save_frequency


    def get_core(self):
        """Get ServerCore instance."""
        return ServerCore(self._items, self._users,
                          self._new_credits_min,
                          self._new_credits_max,
                          self._save_frequency)