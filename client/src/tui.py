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

    def __init__(self):
        """Create TUI instance."""
        self._last_item = None

    def _get_input(self, prompt):
        while True:
            user_input = input(prompt + "\n")
            if user_input == 'quit':
                if self._confirm_exit():
                    return None, False
            elif user_input == 'help':
                self._help()
            else:
                return user_input, True

    def _confirm_exit(self):
        while True:
            user_input = input("Are you sure you want to exit?(y/n)")
            user_input = user_input.strip().lower()
            if user_input in {'q', 'y'}:
                return True
            if user_input == 'n':
                return False
            print("Unexpected symbol")

    def _confirm_action(self, prompt, quitable=False):
        """Ask user if he sure.

        If quitable is set to True, user is given an option to quit.
        In that case, an exception is raised.
        """
        while True:
            user_input = input(prompt + ("(y/n)\n")).strip().lower()
            if user_input == 'y':
                return True
            elif user_input == 'n':
                return False
            elif quitable and user_input == 'q' and self._confirm_exit():
                raise Exception("Quit")
            else:
                print("Unexpected input. Print help for help.")

    def _help(self):
        print("Tips:")
        for command_name, command in self._commands.items():
            description = self._commands_descriptions[command]
            print("{}\t{}".format(command_name, description))
        print("help")
        print("quit")

    def greet(self):
        """Print welcome messange."""
        print("Welcome!")
        self._help()

    def say_name(self, name):
        """Show user his name."""
        print(name)

    def say_wait_for_connection(self):
        """Print message about establishing connection."""
        print("connecting...")

    def say_got_connection(self):
        """Inform user about successfully established connection."""
        print("Connected!")

    def ask_retry_connection(self):
        """Inform user about failed connection and ask retry."""
        return self._confirm_action("Connection failed. Retry?")

    def ask_user_name(self):
        """Get user name."""
        return self._get_input("Enter your login:")

    def confirm_user_name(self, user_name):
        """Ask user to confirm user name."""
        print("No user with name:", user_name)
        ret = (None, None)
        try:
            ret = (self._confirm_action("Create new user?", quitable=True),
                   True)
        except:
            ret = (None, False)
        return ret

    def get_command(self):
        """Get command from user."""
        while True:
            user_input, running = self._get_input("Enter command:")
            if not running:
                return None, False

            new_item = None
            if len(user_input.split()) == 2:
                user_input, new_item = user_input.split()

            if user_input not in self._commands:
                print("Unexpected input. Print help for help.")
            else:
                if new_item:
                    self._last_item = new_item
                return (self._commands[user_input], running)

    @property
    def last_item(self):
        """Get name of last chosen item."""
        return self._last_item

    def show_credits(self, credits_sum):
        """Show user number of his credits."""
        print("Your account:", credits_sum)

    def print_list(self, items):
        """Print list of items."""
        if not items:
            print("Empty")
        for item in items:
            print(item)

    def show_deal_result(self, result):
        """Print result of last user operation.

        Result must be unpackable into two values:
        binary flag, which indicates success of operation
        message for user.
        """
        result, message = result
        if result:
            print("Success!")
        else:
            print("Operation Failed.")
        print(message)

    def confirm_log_out(self):
        """Ask user if he sure he wants to log out."""
        ret = (None, None)
        try:
            ret = (self._confirm_action("Log out?", quitable=True),
                   True)
        except:
            ret = (None, False)
        return ret

    def farewell(self):
        """Print farewell message."""
        print("Thank you for playing!")

# TODO Replace Rust-style quit by exceptions
