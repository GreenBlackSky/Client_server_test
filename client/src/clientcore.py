"""Module contains ClientCore class."""

from shared.commands import Command


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
            Command.GET_CREDITS: self._server.get_credits,
            Command.GET_MY_ITEMS: self._server.get_my_items,
            Command.GET_ALL_ITEMS: self._server.get_all_items,
            Command.PURCHASE_ITEM: lambda:
                self._server.purchase_item(self._ui.last_item),
            Command.SELL_ITEM: lambda:
                self._server.sell_item(self._ui.last_item)
        }

        self._result_retrievers = {
            Command.GET_CREDITS: self._ui.show_credits,
            Command.GET_MY_ITEMS: self._ui.print_list,
            Command.GET_ALL_ITEMS: self._ui.print_list,
            Command.PURCHASE_ITEM: self._ui.show_deal_result,
            Command.SELL_ITEM: self._ui.show_deal_result
        }

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
        if self._server.has_connection():
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
        account_exsits, connected = self._server.has_account(self._user_name)
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
        if self._last_command is Command.LOG_OUT:
            self._state = ClientCore._State.LOGGINIG_OUT

        self._last_result, connected = \
            self._command_executors[self._last_command]

        if not connected:
            self._state = ClientCore._State.CONNECTING
        else:
            self._state = ClientCore._State.RETRIEVING_RESULT

    def _retrieve_result(self):
        # user
        self._result_retrievers[self._last_command](self._last_result)
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
