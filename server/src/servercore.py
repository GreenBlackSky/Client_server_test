"""Module contains ServerCore class."""

from random import randint
from netrequest import Request, Answer


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

        def __init__(self, items_db, users_db,
                        min_limit, max_limit,
                        save_frequency):
            self._items = items_db
            self._users = users_db
            self._new_credits_max = max_limit
            self._new_credits_min = min_limit
            self._user = None
            self._operation_count = 1
            self._save_frequency = save_frequency

            # Data to return on request
            self._get_requset_handlers = {
                Request.Type.GET_NAME: lambda: self._user.name,
                Request.Type.GET_CREDITS: lambda: self._user.credits,
                Request.Type.GET_MY_ITEMS: lambda: self._user.items,
            }

            # Methods to call on request
            self._util_request_handlers = {
                Request.Type.PING: self._ping,
                Request.Type.USER_EXISTS: self._user_exists,
                Request.Type.LOG_IN: self._log_in,
                Request.Type.LOG_OUT: self._log_out,
                Request.Type.GET_ALL_ITEMS: self._get_all_items,
                Request.Type.PURCHASE_ITEM: self._buy_item,
                Request.Type.SELL_ITEM: self._sell_item,
            }

        def process_request(self, request):
            """Process request from client and return answer."""
            self._operation_count = \
                (self._operation_count + 1)%self._save_frequency
            if self._operation_count == 0:
                self._users.commit()

            request_type, data = request.request_type, request.data
            try:
                if request_type in self._get_requset_handlers:
                    return self._handle_get_request(request_type)
                elif request_type in self._util_request_handlers:
                    return self._util_request_handlers[request_type](data)
            except ServerCore.NoSuchItem:
                return Answer(request_type,
                            success=False,
                            message="Not such item: " + data)
            except ServerCore.NoUserLoggedIn:
                return Answer(request_type,
                            success=False,
                            message="Not logged in")

        def _check_user(self):
            if not self._user:
                raise ServerCore.NoUserLoggedIn

        def _check_item(self, item_name):
            if item_name not in self._items:
                raise ServerCore.NoSuchItem

        def _handle_get_request(self, request_type):
            self._check_user()
            return Answer(request_type,
                        data=self._get_requset_handlers[request_type]())

        def _ping(self, _):
            return Answer(Request.Type.PING)

        def _user_exists(self, user_name):
            return Answer(Request.Type.USER_EXISTS,
                        data=(user_name in self._users))

        def _log_in(self, user_name):
            self._users.check_and_add_user(user_name)
            self._user = self._users[user_name]
            self._user.credits += randint(self._new_credits_min,
                                        self._new_credits_max)
            return Answer(Request.Type.LOG_IN)

        def _log_out(self, _):
            request_type = Request.Type.LOG_OUT
            self._check_user()
            self._user = None
            self._users.commit()
            return Answer(request_type)

        def _get_all_items(self, _):
            request_type = Request.Type.GET_ALL_ITEMS
            return Answer(request_type, data=self._items.values())

        def _buy_item(self, item_name):
            request_type = Request.Type.PURCHASE_ITEM
            self._check_user()
            self._check_item(item_name)
            item = self._items[item_name]
            if item.buying_price <= self._user.credits:
                self._user.credits -= item.buying_price
                self._user.items.append(item)
                ret = Answer(request_type, message="Item bought: " + item_name)
            else:
                ret = Answer(request_type,
                            success=False,
                            message="Not enough money")
            self._operation_count += 1
            return ret

        def _sell_item(self, item_name):
            request_type = Request.Type.SELL_ITEM
            self._check_user()
            self._check_item(item_name)
            item = self._items[item_name]
            if item in self._user.items:
                self._user.items.remove(item)
                self._user.credits += item.selling_price
                ret = Answer(request_type, message="Item sold: " + item_name)
            else:
                ret = Answer(request_type,
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

    def get_core(self):
        """Get handler for new client."""
        return self._Handler(self._items, self._users,
                          self._new_credits_min,
                          self._new_credits_max,
                          self._save_frequency)

# TODO add users command to list all users
