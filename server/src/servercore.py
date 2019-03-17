"""Module contains ServerCore class."""

from random import randint
from request import Request, Responce


class ServerCore:
    """Instances of ServerCore generates handlers.

    Generated objects has properties,
    passed to ServerCore itself.
    """

    class NoUserLoggedIn(Exception):
        """Exception to rise when there is no user logged in.

        Rises when logged in user is required to process request.
        """

        pass


    class NoSuchItem(Exception):
        """Exception to rise when no item found by given name."""

        pass


    class _Handler:
        """Class handles clients."""

        def __init__(self, parent):
            self._parent = parent
            self._user = None
            self._operation_count = 1

            # Methods to call on request
            self._request_handlers = {
                Request.Type.PING: self._parent.ping,
                Request.Type.USER_EXISTS: self._parent.user_exists,
                Request.Type.GET_ALL_ITEMS: self._parent.get_all_items,
                Request.Type.LOG_IN: self._log_in,
                Request.Type.LOG_OUT: self._log_out,
                Request.Type.PURCHASE_ITEM: self._buy_item,
                Request.Type.SELL_ITEM: self._sell_item,
                Request.Type.GET_NAME: self._get_user_name,
                Request.Type.GET_CREDITS: self._get_user_credits,
                Request.Type.GET_MY_ITEMS: self._get_user_items
            }

        def process_request(self, request):
            """Process request from client and return responce."""
            self._operation_count = \
                (self._operation_count + 1)%self._parent.save_frequency
            if self._operation_count == 0:
                self._parent.users.commit()

            request_type, data = request.request_type, request.data
            try:
                # if request_type is Request.Type.LOG_IN:
                #     return self._log_in(data)
                # elif request_type is Request.Type.LOG_OUT:
                #     return self._log_out()
                # else:
                #     return self._parent.handle_request_from(user, request)
                return self._request_handlers[request_type](data)
            except ServerCore.NoSuchItem:
                return Responce(request_type,
                                success=False,
                                message="Not such item: " + data)
            except ServerCore.NoUserLoggedIn:
                return Responce(request_type,
                                success=False,
                                message="Not logged in")

        def _check_user(self):
            if not self._user:
                raise ServerCore.NoUserLoggedIn

        def _log_in(self, user_name):
            self._parent.users.check_and_add_user(user_name)
            self._user = self._parent.users[user_name]
            self._user.credits += randint(self._parent.new_credits_min,
                                          self._parent.new_credits_max)
            return Responce(Request.Type.LOG_IN)

        def _log_out(self, _):
            request_type = Request.Type.LOG_OUT
            self._check_user()
            self._user = None
            self._parent.users.commit()
            return Responce(request_type)

#------------------------------------------------------------------------------------

        def _get_user_name(self, _):
            return Responce(Request.Type.GET_NAME, data=self._user.name)

        def _get_user_credits(self, _):
            return Responce(Request.Type.GET_CREDITS, data=self._user.credits)

        def _get_user_items(self, _):
            return Responce(Request.Type.GET_MY_ITEMS, data=self._user.items)

        def _buy_item(self, item_name):
            request_type = Request.Type.PURCHASE_ITEM
            self._check_user()
            self._parent.check_item(item_name)
            item = self._parent.items[item_name]
            if item.buying_price <= self._user.credits:
                self._user.credits -= item.buying_price
                self._user.items.append(item)
                ret = Responce(request_type, message="Item bought: " + item_name)
            else:
                ret = Responce(request_type,
                               success=False,
                               message="Not enough money")
            self._operation_count += 1
            return ret

        def _sell_item(self, item_name):
            request_type = Request.Type.SELL_ITEM
            self._check_user()
            self._parent.check_item(item_name)
            item = self._parent.items[item_name]
            if item in self._user.items:
                self._user.items.remove(item)
                self._user.credits += item.selling_price
                ret = Responce(request_type, message="Item sold: " + item_name)
            else:
                ret = Responce(request_type,
                               success=False,
                               message="No such item")
            self._operation_count += 1
            return ret

    def __init__(self, items_db, users_db,
                       min_limit, max_limit,
                       save_frequency):
        """Create ServerCore."""
        self._items = items_db
        self._users = users_db
        self._new_credits_max = max_limit
        self._new_credits_min = min_limit
        self._save_frequency = save_frequency

    @property
    def items(self):
        """Get items data base."""
        return self._items

    @property
    def users(self):
        """Get users data base."""
        return self._users

    @property
    def save_frequency(self):
        """Get frequency of commits into users data base."""
        return self._save_frequency

    @property
    def new_credits_min(self):
        """Get minimum log in credits sum."""
        return self._new_credits_min

    @property
    def new_credits_max(self):
        """Get maximum log in credits sum."""
        return self._new_credits_max

    def get_core(self):
        """Get handler for new client."""
        return self._Handler(self)

    def check_item(self, item_name):
        """Check if item with given name is exists."""
        if item_name not in self._items:
            raise ServerCore.NoSuchItem

    def get_all_items(self, _):
        """Get list of all items."""
        request_type = Request.Type.GET_ALL_ITEMS
        return Responce(request_type, data=self._items.values())

    def ping(self, _):
        """Answer to ping request."""
        return Responce(Request.Type.PING)

    def user_exists(self, user_name):
        """Check if user under given name does exist in data base."""
        return Responce(Request.Type.USER_EXISTS,
                        data=(user_name in self._users))

# TODO add users command to list all users
