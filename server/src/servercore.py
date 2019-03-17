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

        def process_request(self, request):
            """Process request from client and return responce."""
            request_type, data = request.request_type, request.data
            try:
                if request_type is Request.Type.LOG_IN:
                    return self._log_in(data)
                elif request_type is Request.Type.LOG_OUT:
                    return self._log_out()
                else:
                    return self._parent.handle_request_from(self._user, request)
            except ServerCore.NoSuchItem:
                return Responce(request_type,
                                success=False,
                                message="Not such item: " + data)
            except ServerCore.NoUserLoggedIn:
                return Responce(request_type,
                                success=False,
                                message="Not logged in")

        def _log_in(self, user_name):
            self._parent.users.check_and_add_user(user_name)
            self._user = self._parent.users[user_name]
            self._user.credits += self._parent.get_init_credits()
            return Responce(Request.Type.LOG_IN)

        def _log_out(self):
            request_type = Request.Type.LOG_OUT
            if not self._user:
                raise ServerCore.NoUserLoggedIn
            self._user = None
            self._parent.users.commit()
            return Responce(request_type)

    def __init__(self, items_db, users_db,
                       min_limit, max_limit,
                       save_frequency):
        """Create ServerCore."""
        self._items = items_db
        self._users = users_db
        self._new_credits_max = max_limit
        self._new_credits_min = min_limit
        self._save_frequency = save_frequency
        self._operation_count = 1

        self._request_handlers = {
            Request.Type.PING: self._ping,
            Request.Type.USER_EXISTS: self._user_exists,
            Request.Type.GET_ALL_ITEMS: self._get_all_items,
            Request.Type.GET_NAME: self._get_user_name,
            Request.Type.GET_CREDITS: self._get_user_credits,
            Request.Type.GET_MY_ITEMS: self._get_user_items,
            Request.Type.PURCHASE_ITEM: self._buy_item,
            Request.Type.SELL_ITEM: self._sell_item
        }

    @staticmethod
    def _check_user(user):
        if not user:
            raise ServerCore.NoUserLoggedIn

    def _check_item(self, item_name):
        """Check if item with given name is exists."""
        if item_name not in self._items:
            raise ServerCore.NoSuchItem

    @property
    def users(self):
        """Get users data base."""
        return self._users

    def get_init_credits(self):
        """Get random sum of credits for user initialization."""
        return randint(self._new_credits_min, self._new_credits_max)

    def get_core(self):
        """Get handler for new client."""
        return self._Handler(self)

    def handle_request_from(self, user, request):
        """Handle request for given user."""
        self._operation_count = \
            (self._operation_count + 1)%self._save_frequency
        if self._operation_count == 0:
            self._users.commit()
        return self._request_handlers[request.request_type](user, request.data)

    def _get_all_items(self, *_):
        request_type = Request.Type.GET_ALL_ITEMS
        return Responce(request_type, data=self._items.values())

    def _ping(self, *_):
        return Responce(Request.Type.PING)

    def _user_exists(self, user, user_name):
        return Responce(Request.Type.USER_EXISTS,
                        data=(user_name in self._users))

    def _get_user_name(self, user, _):
        self._check_user(user)
        return Responce(Request.Type.GET_NAME, data=user.name)

    def _get_user_credits(self, user, _):
        self._check_user(user)
        return Responce(Request.Type.GET_CREDITS, data=user.credits)

    def _get_user_items(self, user, _):
        self._check_user(user)
        return Responce(Request.Type.GET_MY_ITEMS, data=user.items)

    def _buy_item(self, user, item_name):
        request_type = Request.Type.PURCHASE_ITEM
        self._check_user(user)
        self._check_item(item_name)
        item = self._items[item_name]
        if item.buying_price <= user.credits:
            user.credits -= item.buying_price
            user.items.append(item)
            ret = Responce(request_type, message="Item bought: " + item_name)
        else:
            ret = Responce(request_type,
                            success=False,
                            message="Not enough money")
        self._operation_count += 1
        return ret

    def _sell_item(self, user, item_name):
        request_type = Request.Type.SELL_ITEM
        self._check_user(user)
        self._check_item(item_name)
        item = self._items[item_name]
        if item in user.items:
            user.items.remove(item)
            user.credits += item.selling_price
            ret = Responce(request_type, message="Item sold: " + item_name)
        else:
            ret = Responce(request_type,
                            success=False,
                            message="No such item")
        self._operation_count += 1
        return ret

# TODO add users command to list all users
