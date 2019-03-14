"""Module contains NetworkClient."""

import socket
from netrequest import Request
from pickle import dumps, loads
from commands import Command
from item import Item
from random import randint


class Account:
    def __init__(self, name):
        self.name = name
        self.credits = 0
        self.items = list()


class NetworkClient:
    """NetworkClient handles connection with server on client side."""

    def __init__(self, server_ip, server_port, timeout):
        """Initialize client.

        On start client will try to connect to given server,
        on given port with given timeout(ms).
        """
        # self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self._socket.connect((host, port))
        # self._socket.settimeout(timeout)
        self.dummy_accounts = dict()
        self.dummy_account = None
        self.dummy_items = {
            "hat": Item("hat", 10, 5),
            "shirt": Item("shirt", 20, 10),
            "pants": Item("pants", 40, 20),
            "boots": Item("boots", 80, 40),
            "shovel": Item("shovel", 160, 80)
        }

    # def _send_request(self, command, data=None):
    #     request = Request(command, data)
    #     self._socket.sendall(dumps(request))

    # def _get_responce(self):
    #     return loads(self._socket.recv(1024))

    def has_connection(self):
        # ret = True
        # try:
        #     self._send_request(Command.PING)
        #     self._get_responce()
        # except:
        #     ret = False
        # return ret
        ret = (randint(1, 5) != 5)
        if not ret:
            self.log_out()
        return ret

    def has_account(self, user_name):
        # connected = True
        # ret = None
        # try:
        #     self._send_request(Command.USER_EXISTS, user_name)
        #     ret = self._get_responce()
        # except:
        #     connected = False
        # return ret, connected
        return user_name in self.dummy_accounts, self.has_connection()

    def get_name(self):
        return self.dummy_account.name,  self.has_connection()

    def log_in(self, user_name):
        self.dummy_accounts[user_name] = \
            self.dummy_accounts.get(user_name, Account(user_name))
        self.dummy_account = self.dummy_accounts[user_name]
        self.dummy_account.credits += 10
        return self.has_connection()

    def get_credits(self):
        if self.dummy_account:
            return self.dummy_account.credits, self.has_connection()

    def get_my_items(self):
        if self.dummy_account:
            return self.dummy_account.items, self.has_connection()

    def get_all_items(self):
        return self.dummy_items.values(), self.has_connection()

    def log_out(self):
        self.dummy_account = None

    def purchase_item(self, item):
        if item not in self.dummy_items:
            return (False, "No such item"), self.has_connection()

        item = self.dummy_items[item]
        if self.dummy_account.credits >= item.buying_price:
            self.dummy_account.credits -= item.buying_price
            self.dummy_account.items.append(item)
            return (True, "Item bought"), self.has_connection()
        return (False, "not enough money"), self.has_connection()

    def sell_item(self, item):
        if item not in self.dummy_items:
            return (False, "No such item"), self.has_connection()

        item = self.dummy_items[item]
        if item not in self.dummy_account.items:
            return (False, "You don't have this item"), self.has_connection()

        self.dummy_account.credits += item.selling_price
        self.dummy_account.items.remove(item)
        return (True, "Item sold"), self.has_connection()
