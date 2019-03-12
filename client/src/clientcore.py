"""Module contains ClientCore class."""

from enum import Enum, auto


# Works as finite-state machine. Most of methods works exclusively with
# user via ui, or with server via network handler.
class ClientCore:
    """Class contains client-side logic.

    Implements interaction between user and server.
    """

    class _Command(Enum):
        GET_CREDITS = auto()
        GET_MY_ITEMS = auto()
        GET_ALL_ITEMS = auto()
        LOG_OUT = auto()

    class _State(Enum):
        CONNECTING = auto()
        ASKING_NAME = auto()
        CHECKING_NAME = auto()
        CONFIRMING_NAME = auto()
        LOGGINIG_IN = auto()
        GETTING_COMMAND = auto()
        EXECUTING_COMMAND = auto()
        RETRIEVING_RESULT = auto()
        LOGGINIG_OUT = auto()
        DISCONNECTING = auto()

    _states = {
        ClientCore._State.CONNECTING: self._connect,
        ClientCore._State.ASKING_NAME: self._ask_name,
        ClientCore._State.CHECKING_NAME: self._check_user_name,
        ClientCore._State.CONFIRMING_NAME: self._confirm_user_name,
        ClientCore._State.LOGGINIG_IN: self._log_in,
        ClientCore._State.GETTING_COMMAND: self._get_command,
        ClientCore._State.EXECUTING_COMMAND: self._execute_command,
        ClientCore._State.RETRIEVING_RESULT: self._retrieve_result,
        ClientCore._State.LOGGINIG_OUT: self._log_out
    }

    def __init__(self, server, ui):
        """Create new ClientCore object.

        Gets network handler and ui handler.
        """
        self._server, self._ui = server, ui
        self._state = ClientCore._State.CONNECTING
        self._user_name = None
        self._last_command = None
        self._last_result = None

    def exec(self):
        """Start exec loop.

        On each iteration object checks user events,
        send them to server and process answear.
        """
        self._ui.greet()
        while self._state is not ClientCore._State.DISCONNECTING:
            states[self._state]()
        self._ui.farewell()

    def _connect(self):
        # both
        self._ui.say_wait_for_connection()
        if self._server.check_connection():
            self._ui.say_got_connection()
            if self._user_name:
                self._state = ClientCore._State.LOGGINIG_IN
            else:
                self._state = ClientCore._State.ASKING_NAME
        elif not self._ui.ask_retry_connection():
            self._state = ClientCore._State.DISCONNECTING

    def _ask_name(self):
        # user
        self._user_name, running = self._ui.ask_user_name()
        if not running:
            self._state = ClientCore._State.DISCONNECTING
        else:
            self._state = ClientCore._State.CHECKING_NAME

    def _check_user_name(self):
        # server
        account_exsits, connected = self._server.check_account(self._user_name)
        if not connected:
            self._state = ClientCore._State.CONNECTING
        elif not account_exsits:
            self._state = ClientCore._State.CONFIRMING_NAME
        else:
            self._state = ClientCore._State.LOGGINIG_IN

    def _confirm_user_name(self):
        # user
        confirm, running = self._ui.confirm_user_name(self._user_name)
        if not running:
            self._state = ClientCore._State.DISCONNECTING
        elif confirm:
            self._state = ClientCore._State.LOGGINIG_IN
        else:
            self._state = ClientCore._State.ASKING_NAME

    def _log_in(self):
        # server
        connected = self._server.log_in(self._user_name)
        if not connected:
            self._state = ClientCore._State.CONNECTING
        else:
            self._state = ClientCore._State.GETTING_COMMAND

    def _get_command(self):
        # user
        self._last_command, running = self._ui.get_command()
        if not running:
            self._state = ClientCore._State.LOGGINIG_OUT
        else:
            self._state = ClientCore._State.EXECUTING_COMMAND

    def _execute_command(self):
        # server
        if self._last_command is ClientCore._Command.GET_CREDITS:
            self._last_result, connected = self._server.get_credits()
        elif self._last_command is ClientCore._Command.GET_MY_ITEMS:
            self._last_result, connected = self._server.get_my_items()
        elif self._last_command is ClientCore._Command.GET_ALL_ITEMS:
            self._last_result, connected = self._server.get_all_items()
        self._state = ClientCore._State.RETRIEVING_RESULT

        if self._last_command is ClientCore._Command.LOG_OUT:
            self._state = ClientCore._State.LOGGINIG_OUT
        if not connected:
            self._state = ClientCore._State.CONNECTING

    def _retrieve_result(self):
        # user
        if self._last_command is ClientCore._Command.GET_CREDITS:
            self._ui.show_credits(self._last_result)
        elif self._last_command is ClientCore._Command.GET_MY_ITEMS:
            self._ui.show_my_items(self._last_result)
        elif self._last_command is ClientCore._Command.GET_ALL_ITEMS:
            self._ui.show_all_items(self._last_result)
        self._state = ClientCore._State.GETTING_COMMAND

    def _log_out(self):
        # both
        confirm, running = self._ui.confirm_log_out()
        if not running:
            self._state = ClientCore._State.DISCONNECTING
        elif confirm:
            self._server.log_out()
            self._state = ClientCore._State.ASKING_NAME
        else:
            self._state = ClientCore._State.GETTING_COMMAND
