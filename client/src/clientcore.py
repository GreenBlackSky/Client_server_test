"""Module contains ClientCore class."""

from netrequest import Request
from enum import Enum


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
        CONNECTING = 0
        ASKING_RECONNECT = 1
        ASKING_NAME = 2
        CHECKING_NAME = 3
        CONFIRMING_NAME = 4
        LOGGINIG_IN = 5
        GETTING_COMMAND = 6
        EXECUTING_COMMAND = 7
        RETRIEVING_RESULT = 8
        LOGGINIG_OUT = 9
        DISCONNECTING = 10

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
        self._server.execute(Request.Type.PING)
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
        answer = self._server.execute(Request.Type.USER_EXISTS,
                                      self._user_name)
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
        self._server.execute(Request.Type.LOG_IN, self._user_name)
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
            self._last_result = self._server.execute(self._last_command,
                                                     self._ui.last_item)
            self._state = ClientCore._State.RETRIEVING_RESULT

    def _retrieve_result(self):
        # user
        self._ui.show_result(self._last_result)
        self._state = ClientCore._State.GETTING_COMMAND

    def _log_out(self):
        # both
        confirm = self._ui.confirm_log_out()
        if confirm:
            self._server.execute(Request.Type.LOG_OUT)
            self._state = ClientCore._State.ASKING_NAME
        else:
            self._state = ClientCore._State.GETTING_COMMAND
