"""Module contains commands.

Commands are used in communication between parts of application
"""

from enum import Enum, auto


class Command(Enum):
    """Enum, which contains commands."""

    GET_CREDITS = auto()
    GET_MY_ITEMS = auto()
    GET_ALL_ITEMS = auto()
    PURCHASE_ITEM = auto()
    SELL_ITEM = auto()
    LOG_OUT = auto()
