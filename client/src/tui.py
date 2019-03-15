"""Text User Interface."""

from netrequest import Request


class TUI:
    """TUI is used to pass information between app and user.

    Most of methods could be replaced by more direct calls, I know.
    BUT some another implementation may use entirly different mechaincs.
    TUI was meant to be replaced by any other UI class,
    which implements necessary methods.
    """

    _commands = {
        "name": Request.Type.GET_NAME,
        "credits": Request.Type.GET_CREDITS,
        "items": Request.Type.GET_MY_ITEMS,
        "market": Request.Type.GET_ALL_ITEMS,
        "buy": Request.Type.PURCHASE_ITEM,
        "sell": Request.Type.SELL_ITEM,
        "leave": Request.Type.LOG_OUT
    }

    _commands_descriptions = {
        Request.Type.GET_NAME: "show name of current user",
        Request.Type.GET_CREDITS: "show credits you have",
        Request.Type.GET_MY_ITEMS: "show items you have",
        Request.Type.GET_ALL_ITEMS: "show all aceccible items",
        Request.Type.PURCHASE_ITEM: "buy item, usage: buy <item_name>",
        Request.Type.SELL_ITEM: "sell item, usage: sell <item_name>",
        Request.Type.LOG_OUT: "log out"
    }

# Util

    def __init__(self):
        """Create TUI instance."""
        self._last_item = None
        self._result_retrievers = {
            Request.Type.GET_CREDITS: self._show_credits,
            Request.Type.GET_MY_ITEMS: self._print_list,
            Request.Type.GET_ALL_ITEMS: self._print_list,
            Request.Type.PURCHASE_ITEM: self._show_deal_result,
            Request.Type.SELL_ITEM: self._show_deal_result,
            Request.Type.GET_NAME: self._say_name
        }

    def _get_input(self, prompt):
        while True:
            user_input = input(prompt + "\n")
            if user_input == 'quit':
                self._confirm_exit()
            elif user_input == 'help':
                self._help()
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

    def _help(self):
        print("Tips:")
        for command_name, command in self._commands.items():
            description = self._commands_descriptions[command]
            print("{}\t{}".format(command_name, description))
        print("help")
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
        """Inform user about failed connection and ask retry."""
        return self._confirm_action("Connection failed. Retry?")

    def ask_user_name(self):
        """Get user name."""
        return self._get_input("Enter your login:")

    def confirm_user_name(self, user_name):
        """Ask user to confirm user name."""
        print("No user with name:", user_name)
        return self._confirm_action("Create new user?")

    def get_command(self):
        """Get command from user."""
        while True:
            user_input = self._get_input("Enter command:")

            new_item = None
            if len(user_input.split()) >= 2:
                user_input, *new_item = user_input.split()
                new_item = " ".join(new_item)

            if user_input not in self._commands:
                print("Unexpected input. Print help for help.")
            else:
                if new_item:
                    self._last_item = new_item
                return self._commands[user_input]

    def confirm_log_out(self):
        """Ask user if he sure he wants to log out."""
        return self._confirm_action("Log out?")

# Output methods

    def show_result(self, result):
        self._result_retrievers[result.request_type](result)

    def _say_name(self, result):
        """Show user his name."""
        if result.success:
            print(result.data)
        else:
            print(result.message)

    def _show_credits(self, result):
        """Show user number of his credits."""
        print("Your account:", result.data)

    def _print_list(self, result):
        """Print list of items."""
        if not result.success:
            print(result.message)
        elif not result.data:
            print("Empty")
        else:
            for item in result.data:
                print(item)

    def _show_deal_result(self, result):
        """Print result of last user operation."""
        if result.success:
            print("Success!")
        else:
            print("Operation Failed.")
        print(result.message)
