"""Module contains ClientCore class."""

from request import Request
from enum import Enum


class ClientCore:
    """Class contains client-side logic.

    Implements interaction between user and server.
    Works as finite-state machine.
    I know it could have been implemented without states, using direct calls.
    But that is exaclty what is called spaghetti-code =)
    Most of methods works exclusively with user via ui,
    or with server via network handler.
    Class is designed so you never have to pay for what you haven't asked for.
    It means no cache, only straight and simple request-response behavior.
    """

    class _State(Enum):
        CONNECTING = 0
        ASKING_RECONNECT = 1
        ASKING_NAME = 2
        LOGGINIG_IN = 3
        GETTING_COMMAND = 4
        EXECUTING_COMMAND = 5
        RETRIEVING_RESULT = 6
        LOGGINIG_OUT = 7
        DISCONNECTING = 8

    def __init__(self, server, ui):
        """Create new ClientCore object.

        Gets network handler and ui handler.
        """
        self._server, self._ui = server, ui
        self._ui.set_server(self._server)
        self._state = ClientCore._State.CONNECTING
        self._user_name = None
        self._last_command = None
        self._last_result = None

        self._states = {
            ClientCore._State.CONNECTING: self._connect,
            ClientCore._State.ASKING_RECONNECT: self._ask_reconnect,
            ClientCore._State.ASKING_NAME: self._ask_name,
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
        self._state = ClientCore._State.LOGGINIG_IN

    def _log_in(self):
        # both
        response = self._server.execute(Request.Type.LOG_IN, self._user_name)
        self._ui.show_result(response)
        if response.success:
            self._state = ClientCore._State.GETTING_COMMAND
        else:
            self._state = ClientCore._State.ASKING_NAME

    def _get_command(self):
        # user
        self._last_command = self._ui.get_command()
        self._state = ClientCore._State.EXECUTING_COMMAND

    def _execute_command(self):
        # server
        if self._last_command is Request.Type.LOG_OUT:
            self._state = ClientCore._State.LOGGINIG_OUT
        else:
            self._last_result = self._server.execute(
                self._last_command,
                self._ui.last_item
            )
            self._state = ClientCore._State.RETRIEVING_RESULT

    def _retrieve_result(self):
        # user
        self._ui.show_result(self._last_result)
        self._state = ClientCore._State.GETTING_COMMAND

    def _log_out(self):
        # both
        self._server.execute(Request.Type.LOG_OUT)
        self._state = ClientCore._State.ASKING_NAME
