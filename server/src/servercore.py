"""Module contains ServerCore class."""

from random import randint
from request import Request, Responce


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
            """Process request from client and return responce."""
            request_type, data = request.request_type, request.data
            if request_type is Request.Type.LOG_IN:
                return self._log_in(data)
            elif request_type is Request.Type.LOG_OUT:
                return self._log_out()
            else:
                return self._parent.handle_request_from(self._user, request)

        def _log_in(self, user_name):
            if self._parent.user_is_activated(user_name):
                return Responce(Request.Type.LOG_IN,
                                success=False,
                                message="User already online")
            self._user = self._parent.users[user_name]
            self._user.credits += self._parent.get_init_credits()
            self._parent.activate_user(user_name)
            return Responce(Request.Type.LOG_IN)

        def _log_out(self):
            request_type = Request.Type.LOG_OUT
            if not self._user:
                raise ServerCore.NoUserLoggedIn
            self._parent.deactivate_user(self._user.name)
            self._user = None
            self._parent.users.commit()
            return Responce(request_type)

        def deactivate_user(self):
            if self._user:
                self._parent.deactivate_user(self._user.name)

    def __init__(self, items_db, users_db,
                 min_limit, max_limit,
                 save_frequency,
                 simultanious_log_ins):
        """Create ServerCore."""
        self._items = items_db
        self._users = users_db

        self._new_credits_max = max_limit
        self._new_credits_min = min_limit

        self._save_frequency = save_frequency
        self._operation_count = 1

        self._simultanious_log_ins = simultanious_log_ins
        self._active_users_names = set()

        self._request_handlers = {
            Request.Type.PING: self._ping,
            Request.Type.GET_ALL_USERS: self._get_all_users,            
            Request.Type.USER_EXISTS: self._user_exists,
            Request.Type.GET_ALL_ITEMS: self._get_all_items,
            Request.Type.GET_NAME: self._get_user_name,
            Request.Type.GET_CREDITS: self._get_user_credits,
            Request.Type.GET_MY_ITEMS: self._get_user_items,
            Request.Type.PURCHASE_ITEM: self._buy_item,
            Request.Type.SELL_ITEM: self._sell_item
        }

    @staticmethod
    def _no_user_responce(request_type):
        return Responce(request_type,
                        success=False,
                        message="Not logged in")

    @staticmethod
    def _no_item_responce(request_type, item_name):
        return Responce(request_type,
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
        self._operation_count = \
            (self._operation_count + 1)%self._save_frequency
        if self._operation_count == 0:
            self._users.commit()
        return self._request_handlers[request.request_type](user, request.data)

    def _get_all_users(self, *_):
        request_type = Request.Type.GET_ALL_USERS
        return Responce(request_type, data=self._users.keys())

    def _get_all_items(self, *_):
        request_type = Request.Type.GET_ALL_ITEMS
        return Responce(request_type, data=self._items.values())

    def _ping(self, *_):
        return Responce(Request.Type.PING)

    def _user_exists(self, user, user_name):
        return Responce(Request.Type.USER_EXISTS,
                        data=(user_name in self._users))

    def _get_user_name(self, user, _):
        if not user:
            return self._no_user_responce(Requets.Type.GET_NAME)
        return Responce(Request.Type.GET_NAME, data=user.name)

    def _get_user_credits(self, user, _):
        if not user:
            return self._no_user_responce(Requets.Type.GET_CREDITS)
        return Responce(Request.Type.GET_CREDITS, data=user.credits)

    def _get_user_items(self, user, _):
        if not user:
            return self._no_user_responce(Requets.Type.GET_MY_ITEMS)
        return Responce(Request.Type.GET_MY_ITEMS, data=user.items)

    def _buy_item(self, user, item_name):
        request_type = Request.Type.PURCHASE_ITEM
        if not user:
            return self._no_user_responce(request_type)
        if item_name not in self._items:
            return self._no_item_responce(request_type, item_name)
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
        if not user:
            return self._no_user_responce(request_type)
        if item_name not in self._items:
            return self._no_item_responce(request_type, item_name)
        item = self._items[item_name]
        if item in user.items:
            user.items.remove(item)
            user.credits += item.selling_price
            ret = Responce(request_type, message="Item sold: " + item_name)
        else:
            ret = Responce(request_type,
                           success=False,
                           message="You don't have " + item_name)
        self._operation_count += 1
        return ret
