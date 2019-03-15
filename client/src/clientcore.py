"""Module contains ClientCore class."""

from netrequest import Request
from enum import Enum, auto


class ClientCore:
    """Class contains client-side logic.

    Implements interaction between user and server.
    Works as finite-state machine.
    I know it could have been implemented without states, using direct calls.
    But that is exaclty what is called spaghetti-code =)
    Most of methods works exclusively with user via ui,
    or with server via network handler.
    """

    class _State(Enum):
        CONNECTING = auto()
        ASKING_RECONNECT = auto()
        ASKING_NAME = auto()
        CHECKING_NAME = auto()
        CONFIRMING_NAME = auto()
        LOGGINIG_IN = auto()
        GETTING_COMMAND = auto()
        EXECUTING_COMMAND = auto()
        RETRIEVING_RESULT = auto()
        LOGGINIG_OUT = auto()
        DISCONNECTING = auto()

    def __init__(self, server, ui):
        """Create new ClientCore object.

        Gets network handler and ui handler.
        """
        self._server, self._ui = server, ui
        self._state = ClientCore._State.CONNECTING
        self._user_name = None
        self._last_command = None
        self._last_result = None

        self._states = {
            ClientCore._State.CONNECTING: self._connect,
            ClientCore._State.ASKING_RECONNECT: self._ask_reconnect,
            ClientCore._State.ASKING_NAME: self._ask_name,
            ClientCore._State.CHECKING_NAME: self._check_user_name,
            ClientCore._State.CONFIRMING_NAME: self._confirm_user_name,
            ClientCore._State.LOGGINIG_IN: self._log_in,
            ClientCore._State.GETTING_COMMAND: self._get_command,
            ClientCore._State.EXECUTING_COMMAND: self._execute_command,
            ClientCore._State.RETRIEVING_RESULT: self._retrieve_result,
            ClientCore._State.LOGGINIG_OUT: self._log_out
        }

        self._command_executors = {
            Request.Type.GET_NAME: self._server.get_name,
            Request.Type.GET_CREDITS: self._server.get_credits,
            Request.Type.GET_MY_ITEMS: self._server.get_my_items,
            Request.Type.GET_ALL_ITEMS: self._server.get_all_items,
            Request.Type.PURCHASE_ITEM: lambda:
                self._server.purchase_item(self._ui.last_item),
            Request.Type.SELL_ITEM: lambda:
                self._server.sell_item(self._ui.last_item)
        }

        self._result_retrievers = {
            Request.Type.GET_CREDITS: self._ui.show_credits,
            Request.Type.GET_MY_ITEMS: self._ui.print_list,
            Request.Type.GET_ALL_ITEMS: self._ui.print_list,
            Request.Type.PURCHASE_ITEM: self._ui.show_deal_result,
            Request.Type.SELL_ITEM: self._ui.show_deal_result,
            Request.Type.GET_NAME: self._ui.say_name
        }

    def exec(self):
        """Start exec loop.

        On each iteration object checks user events,
        send them to server and process answear.
        """
        self._ui.greet()
        while self._state is not ClientCore._State.DISCONNECTING:
            try:
                self._states[self._state]()
            except SystemExit:
                self._state = ClientCore._State.DISCONNECTING
            except (EOFError, ConnectionError):
                self._state = ClientCore._State.ASKING_RECONNECT
        self._ui.farewell()

    def _connect(self):
        # both
        self._ui.say_wait_for_connection()
        self._server.reconnect()
        self._server.ping()
        self._ui.say_got_connection()
        if self._user_name:
            self._state = ClientCore._State.LOGGINIG_IN
        else:
            self._state = ClientCore._State.ASKING_NAME

    def _ask_reconnect(self):
        # user
        if self._ui.ask_retry_connection():
            self._state = ClientCore._State.CONNECTING
        else:
            self._state = ClientCore._State.DISCONNECTING

    def _ask_name(self):
        # user
        self._user_name = self._ui.ask_user_name()
        self._state = ClientCore._State.CHECKING_NAME

    def _check_user_name(self):
        # server
        answer = self._server.has_user(self._user_name)
        if not answer.data:
            self._state = ClientCore._State.CONFIRMING_NAME
        else:
            self._state = ClientCore._State.LOGGINIG_IN

    def _confirm_user_name(self):
        # user
        confirm = self._ui.confirm_user_name(self._user_name)
        if confirm:
            self._state = ClientCore._State.LOGGINIG_IN
        else:
            self._state = ClientCore._State.ASKING_NAME

    def _log_in(self):
        # server
        self._server.log_in(self._user_name)
        self._state = ClientCore._State.GETTING_COMMAND

    def _get_command(self):
        # user
        self._last_command = self._ui.get_command()
        self._state = ClientCore._State.EXECUTING_COMMAND

    def _execute_command(self):
        # server
        if self._last_command is Request.Type.LOG_OUT:
            self._state = ClientCore._State.LOGGINIG_OUT
        else:
            self._last_result = self._command_executors[self._last_command]()
            self._state = ClientCore._State.RETRIEVING_RESULT

    def _retrieve_result(self):
        # user
        self._result_retrievers[self._last_command](self._last_result)
        self._state = ClientCore._State.GETTING_COMMAND

    def _log_out(self):
        # both
        confirm = self._ui.confirm_log_out()
        if confirm:
            self._server.log_out()
            self._state = ClientCore._State.ASKING_NAME
        else:
            self._state = ClientCore._State.GETTING_COMMAND

# TODO It seems we have bug in log_in
