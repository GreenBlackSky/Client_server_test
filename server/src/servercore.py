"""Module contains ServerCore class."""

from random import randint
from request import Request, Response


class ServerCore:
    """Instances of ServerCore generates handlers.

    Generated objects has properties,
    passed to ServerCore itself.
    """

    class _Handler:
        """Class handles clients."""

        def __init__(self, parent):
            self._parent = parent
            self._user = None

        def process_request(self, request):
            """Process request from client and return response."""
            request_type, data = request.request_type, request.data
            if request_type is Request.Type.LOG_IN:
                return self._log_in(data)
            elif request_type is Request.Type.LOG_OUT:
                return self._log_out()
            else:
                return self._parent.handle_request_from(self._user, request)

        def _log_in(self, user_name):
            if self._parent.user_is_activated(user_name):
                return Response(Request.Type.LOG_IN,
                                success=False,
                                message="User already online")
            self._user = self._parent.users[user_name]
            self._user.credits += self._parent.get_init_credits()
            self._parent.activate_user(user_name)
            return Response(Request.Type.LOG_IN)

        def _log_out(self):
            request_type = Request.Type.LOG_OUT
            if not self._user:
                return Response(request_type,
                                success=False,
                                message="Not logged in")
            self._parent.deactivate_user(self._user.name)
            self._user = None
            self._parent.users.commit()
            return Response(request_type)

        def deactivate_user(self):
            if self._user:
                self._parent.deactivate_user(self._user.name)

    def __init__(self, items_db, users_db,
                 min_limit, max_limit,
                 save_frequency,
                 simultanious_log_ins):
        """Create ServerCore.

        items_db and users_db stands for data bases
        with users and items respectively.

        min_limit and max_limit are bonds for user initialization reward.

        save_frequency is how many operations must take place between
        automatic commits. Operations from each user counts.

        simultanious_log_ins is binary flag, which allows or forbide
        multiple users log in into one account simultaniously.
        """
        self._items = items_db
        self._users = users_db

        self._new_credits_max = max_limit
        self._new_credits_min = min_limit

        self._save_frequency = save_frequency
        self._operation_count = 1

        self._simultanious_log_ins = simultanious_log_ins
        self._active_users_names = set()

        self._plain_requests = {
            Request.Type.GET_ALL_USERS: lambda: self._users.values(),
            Request.Type.GET_ALL_USERS_NAMES: lambda: self._users.keys(),
            Request.Type.GET_ALL_ITEMS: lambda: self._items.values(),
            Request.Type.GET_ALL_ITEMS_NAMES: lambda: self._items.keys(),
            Request.Type.PING: lambda: None,
        }

        self._user_requests = {
            Request.Type.GET_CURRENT_USER: lambda user: user,
            Request.Type.GET_CURRENT_USER_NAME: lambda user: user.name,
            Request.Type.GET_CREDITS: lambda user: user.credits,
            Request.Type.GET_USER_ITEMS_NAMES: lambda user: user.items,
            Request.Type.GET_USER_ITEMS: lambda user: {item.name: item
                                                       for item in user.items}
        }

        self._complex_requests = {
            Request.Type.USER_EXISTS: lambda _, name:
                Response(Request.Type.USER_EXISTS, data=(name in self._users)),
            Request.Type.GET_USER: self._get_user,
            Request.Type.GET_ITEM: self._get_item,
            Request.Type.USER_HAS: self._user_has,
            Request.Type.PURCHASE_ITEM: self._buy_item,
            Request.Type.SELL_ITEM: self._sell_item
        }

    @staticmethod
    def _no_user_response(request_type):
        return Response(request_type,
                        success=False,
                        message="Not logged in")

    @staticmethod
    def _no_item_response(request_type, item_name):
        return Response(request_type,
                        success=False,
                        message="Not such item: " + item_name)

    @property
    def users(self):
        """Get users data base."""
        return self._users

    def activate_user(self, user_name):
        """Mark user by given name as active.

        Works only if simultanious_log_ins is set to False.
        """
        if not self._simultanious_log_ins:
            self._active_users_names.add(user_name)

    def user_is_activated(self, user_name):
        """Check if user by given name is marked as active.

        Works only if simultanious_log_ins is set to False.
        """
        return not self._simultanious_log_ins and \
            user_name in self._active_users_names

    def deactivate_user(self, user_name):
        """Mark user by given name as inactive.

        Works only if simultanious_log_ins is set to False.
        """
        if not self._simultanious_log_ins:
            self._active_users_names.remove(user_name)
        self._users.commit()

    def get_init_credits(self):
        """Get random sum of credits for user initialization."""
        return randint(self._new_credits_min, self._new_credits_max)

    def get_handler(self):
        """Get handler for new client."""
        return self._Handler(self)

    def handle_request_from(self, user, request):
        """Handle request for given user."""
        request_type = request.request_type
        if request_type in self._plain_requests:
            ret = Response(request_type,
                           data=self._plain_requests[request_type]())
        elif request_type in self._user_requests and not user:
            ret = self._no_user_response(request_type)
        elif request_type in self._user_requests:
            ret = Response(request_type,
                           data=self._user_requests[request_type](user))
        else:
            ret = self._complex_requests[request_type](user, request.data)

        if ret.success:
            self._operation_count = \
                (self._operation_count + 1) % self._save_frequency
            if self._operation_count == 0:
                self._users.commit()

        return ret

    def _user_has(self, user, item_name):
        if not user:
            return self._no_user_response(Request.Type.USER_HAS)

        if not item_name:
            return Response(Request.Type.USER_HAS, success=False,
                            message="No item")

        if item_name not in self._items:
            return self._no_item_response(Request.Type.USER_HAS, item_name)

        if item_name not in user.items:
            ret = 0
        else:
            ret = user.items[item_name]
        return Response(Request.Type.USER_HAS, data=ret)

    def _get_item(self, user, item_name):
        if item_name not in self._items:
            return self._no_item_response(Request.Type.GET_ITEM, item_name)

        return Response(Request.Type.GET_ITEM, data=self._items[item_name])

    def _get_user(self, user, user_name):
        if user_name not in self._users:
            return Response(Request.Type.GET_USER,
                            success=False,
                            message="No such user")
        return Response(Request.Type.GET_USER, data=self._users[user_name])

    def _buy_item(self, user, item_name):
        request_type = Request.Type.PURCHASE_ITEM
        if not user:
            return self._no_user_response(request_type)

        if item_name not in self._items:
            return self._no_item_response(request_type, item_name)

        item = self._items[item_name]
        if item.buying_price > user.credits:
            return Response(request_type,
                            success=False,
                            message="Not enough money")

        user.credits -= item.buying_price
        user.items[item_name] = user.items.get(item_name, 0) + 1
        self._operation_count += 1
        return Response(request_type, message="Item bought: " + item_name)

    def _sell_item(self, user, item_name):
        request_type = Request.Type.SELL_ITEM
        if not user:
            return self._no_user_response(request_type)

        if item_name not in self._items:
            return self._no_item_response(request_type, item_name)

        item = self._items[item_name]
        if item_name not in user.items:
            return Response(request_type,
                            success=False,
                            message="You don't have " + item_name)

        user.items[item_name] -= 1
        if user.items[item_name] == 0:
            user.items.pop(item_name)
        user.credits += item.selling_price
        self._operation_count += 1
        return Response(request_type, message="Item sold: " + item_name)

# TODO buy number of items
