"""Text User Interface."""

from request import Request


class TUI:
    """TUI is used to pass information between app and user.

    Most of methods could be replaced by more direct calls, I know.
    BUT some another implementation may use entirly different mechaincs.
    TUI was meant to be replaceable by any other UI class,
    which implements necessary methods.
    """

    _commands = {
        "users": Request.Type.GET_ALL_USERS,
        "name": Request.Type.GET_NAME,
        "credits": Request.Type.GET_CREDITS,
        "items": Request.Type.GET_MY_ITEMS,
        "market": Request.Type.GET_ALL_ITEMS,
        "buy": Request.Type.PURCHASE_ITEM,
        "sell": Request.Type.SELL_ITEM,
        "leave": Request.Type.LOG_OUT
    }

    _commands_descriptions = {
        Request.Type.GET_ALL_USERS: "show list of all users",
        Request.Type.GET_NAME: "show name of current user",
        Request.Type.GET_CREDITS: "show credits you have",
        Request.Type.GET_MY_ITEMS: "show items you have",
        Request.Type.GET_ALL_ITEMS: "show all aceccible items",
        Request.Type.PURCHASE_ITEM: "buy item, usage: buy <item_name>",
        Request.Type.SELL_ITEM: "sell item, usage: sell <item_name>",
        Request.Type.LOG_OUT: "log out"
    }

    _need_confirmation = {
        Request.Type.PURCHASE_ITEM: "Are you sure you want to buy it?",
        Request.Type.SELL_ITEM: "Are you sure you want to sell it?",
        Request.Type.LOG_OUT: "Are you sure you want to log out?",
    }

# Util

    def __init__(self):
        """Create TUI instance."""
        self._last_item = None
        self._server = None
        self._result_retrievers = {
            Request.Type.GET_ALL_USERS: self._print_list,
            Request.Type.LOG_IN: self._show_log_in_result,
            Request.Type.GET_NAME: self._say_name,
            Request.Type.GET_CREDITS: self._show_account,
            Request.Type.GET_MY_ITEMS: self._print_list,
            Request.Type.GET_ALL_ITEMS: self._print_list,
            Request.Type.PURCHASE_ITEM: self._show_deal_result,
            Request.Type.SELL_ITEM: self._show_deal_result
        }

    def set_server(self, server):
        """Set server.

        Any object with link to actual server will do.
        """
        self._server = server

    def _get_input(self, prompt):
        while True:
            user_input = input(prompt + "\n")
            if user_input == 'quit':
                self._confirm_exit()
            elif user_input.startswith('help'):
                self._help(user_input.replace("help", "", 1).strip())
            else:
                return user_input

    def _confirm_exit(self):
        """Throw a SystemExit exception if user confirms exit."""
        while True:
            user_input = input("Are you sure you want to exit?(y/n)")
            user_input = user_input.strip().lower()
            if user_input == 'y':
                raise SystemExit
            elif user_input == 'n':
                return
            else:
                print("Unexpected symbol")

    def _confirm_action(self, prompt):
        """Ask user if he sure."""
        while True:
            user_input = input(prompt + ("(y/n)\n")).strip().lower()
            if user_input == 'y':
                return True
            elif user_input == 'n':
                return False
            elif user_input == 'quit':
                self._confirm_exit()
            else:
                print("Unexpected input. Print help for help.")

    def _help(self, command=None):
        if command:
            if command in self._commands:
                request_type = self._commands[command]
                description = self._commands_descriptions[request_type]
                print(command + ": " + description)
            elif command == "help":
                print("help\tprint tips or command help. Usage: help [<command>]")
            elif command == "quit":
                print(command + ": Exit game")
            else:
                print(command + ": unknown command")
        else:
            print("Tips:")
            for command_name, command in self._commands.items():
                description = self._commands_descriptions[command]
                print("{}\t{}".format(command_name, description))
            print("help\tprint tips or command help. Usage: help [<command>]")
            print("quit")

    @property
    def last_item(self):
        """Get name of last chosen item."""
        return self._last_item

# Decoration methods (to create mood)

    def greet(self):
        """Print welcome messange."""
        print("Welcome!")
        self._help()        

    def say_wait_for_connection(self):
        """Print message about establishing connection."""
        print("connecting...")

    def say_got_connection(self):
        """Inform user about successfully established connection."""
        print("Connected!")

    def farewell(self):
        """Print farewell message."""
        print("Thank you for playing!")

# Input methods

    def ask_retry_connection(self):
        """Inform user about failed connection and ask retry.

        May rise SystemExit exception."""
        return self._confirm_action("Connection failed. Retry?")

    def ask_user_name(self):
        """Get user name.

        May rise SystemExit exception."""
        while True:
            user_name = self._get_input("Enter your login:")
            if not user_name:
                print("Empty login")
            elif user_name == "users":
                responce = self._server.execute(Request.Type.GET_ALL_USERS)
                self._print_list(responce)
            else:
                responce = self._server.execute(Request.Type.USER_EXISTS, user_name)
                if responce.data or \
                     self._confirm_action("No user with name: " + \
                                          user_name + \
                                          "\nCreate new user?"):
                    return user_name

    def get_command(self):
        """Get command from user.

        May rise SystemExit exception."""
        while True:
            user_input = self._get_input("Enter command:")

            new_item = None
            if user_input.count(" ") >= 1:
                user_input, new_item = user_input.split(" ", 1)

            if user_input not in self._commands:
                print("Unexpected input. Print help for help.")
                return

            command = self._commands[user_input]
            if command not in self._need_confirmation or \
                    self._confirm_action(self._need_confirmation[command]):
                if new_item:
                    self._last_item = new_item
                return self._commands[user_input]

# Output methods

    def show_result(self, responce):
        """Show user responce from server."""
        self._result_retrievers[responce.request_type](responce)

    def _show_log_in_result(self, responce):
        if responce.success:
            print("User logged in")
            responce = self._server.execute(Request.Type.GET_CREDITS)
            print("You have", responce.data, "credits")

        else:
            print(responce.message)

    def _say_name(self, responce):
        if responce.success:
            print(responce.data)
        else:
            print(responce.message)

    def _show_account(self, responce):
        if responce.success:
            print("Your account:", responce.data)
        else:
            print(responce.message)

    def _show_deal_result(self, responce):
        if responce.success:
            print("Success!")
        else:
            print(responce.message)
        
    def _print_list(self, responce):
        if not responce.success:
            print(responce.message)
        elif not responce.data:
            print("Empty")
        else:
            for item in responce.data:
                print(item)

# TODO manipulate users from admin account
# TODO add About item command
