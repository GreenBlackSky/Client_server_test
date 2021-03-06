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
        "users": Request.Type.GET_ALL_USERS_NAMES,
        "name": Request.Type.GET_CURRENT_USER_NAME,
        "credits": Request.Type.GET_CREDITS,
        "items": Request.Type.GET_USER_ITEMS_NAMES,
        "market": Request.Type.GET_ALL_ITEMS,
        "price": Request.Type.GET_ITEM,
        "has": Request.Type.USER_HAS,
        "buy": Request.Type.PURCHASE_ITEM,
        "sell": Request.Type.SELL_ITEM,
        "leave": Request.Type.LOG_OUT
    }

    _commands_descriptions = {
        Request.Type.GET_ALL_USERS_NAMES: "show list of all users",
        Request.Type.GET_CURRENT_USER_NAME: "show name of current user",
        Request.Type.GET_CREDITS: "show credits you have",
        Request.Type.GET_USER_ITEMS_NAMES: "show items you have",
        Request.Type.GET_ALL_ITEMS: "show all aceccible items",
        Request.Type.GET_ITEM: "show price of item, usage: price <item_name>",
        Request.Type.USER_HAS:
            "check how much of given item user has, usage: find <item_name>",
        Request.Type.PURCHASE_ITEM:
            "buy item, usage: buy <item_name> [amount]",
        Request.Type.SELL_ITEM: "sell item, usage: sell <item_name> [amount]",
        Request.Type.LOG_OUT: "log out"
    }

# Util

    def __init__(self):
        """Create TUI instance."""
        self._last_item = None
        self._server = None
        self._result_retrievers = {
            Request.Type.GET_ALL_USERS_NAMES: self._print_list,
            Request.Type.LOG_IN: self._show_log_in_result,
            Request.Type.GET_CURRENT_USER_NAME: self._show_response,
            Request.Type.GET_CREDITS: self._show_account,
            Request.Type.GET_USER_ITEMS_NAMES: self._print_dict,
            Request.Type.GET_ITEM: self._show_response,
            Request.Type.USER_HAS: self._show_response,
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
            if user_input == 'quit' or user_input == 'q':
                self._confirm_exit()
            elif user_input.startswith('help'):
                self._help(user_input.replace("help", "", 1).strip())
            else:
                return user_input

    def _confirm_exit(self):
        """Throw a SystemExit exception if user confirms exit."""
        while True:
            user_input = input("Are you sure you want to exit?(y/n)\n")
            user_input = user_input.strip().lower()
            if user_input == 'y' or user_input == 'q':
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
            elif user_input == 'quit' or user_input == 'q':
                self._confirm_exit()
            elif user_input.startswith('help '):
                self._help(user_input[5:])
            else:
                print("Unexpected input. Print help for help.")

    def _help(self, command=None):
        if command:
            if command in self._commands:
                request_type = self._commands[command]
                description = self._commands_descriptions[request_type]
                print(command + ": " + description)
            elif command == "help":
                print("help\tprint tips or command help. \
                       Usage: help <command>")
            elif command == "quit" or command == 'q':
                print(command + ": Exit game")
            else:
                print(command + ": unknown command")
        else:
            print("Tips:")
            for command_name, command in self._commands.items():
                description = self._commands_descriptions[command]
                print(f"{command_name}\t{description}")
            print("help\tprint tips or command help. Usage: help <command>")
            print("quit, q")

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

        May rise SystemExit exception.
        """
        return self._confirm_action("Connection failed. Retry?")

    def ask_user_name(self):
        """Get user name.

        May rise SystemExit exception.
        """
        while True:
            user_name = self._get_input("Enter your login:")
            if not user_name:
                print("Empty login")
            elif user_name == "users":
                response = self._server.execute(
                    Request.Type.GET_ALL_USERS_NAMES
                )
                self._print_list(response)
            else:
                response = self._server.execute(
                    Request.Type.USER_EXISTS,
                    user_name
                )
                if response.data or self._confirm_action(
                    f"No user with name: {user_name}\nCreate new user?"
                ):
                    return user_name

    def get_command(self):
        """Get command from user.

        May rise SystemExit exception.
        """
        while True:
            user_input = self._get_input("Enter command:")
            new_item = None

            if user_input.count(" ") >= 1:
                user_input, new_item = user_input.split(" ", 1)

            if user_input not in self._commands:
                print("Unexpected input. Print help for help.")
                continue

            command = self._commands[user_input]
            self._last_item = new_item

            if command is Request.Type.LOG_OUT and not self._confirm_action(
                "Are you sure you want to log out?"
            ) or (
                command is Request.Type.PURCHASE_ITEM and not self._buy_item()
            ) or (
                command is Request.Type.SELL_ITEM and not self._sell_item()
            ):
                continue

            return command

    def _buy_item(self):
        """Check if user can and wish to buy last item."""
        try:
            item_name, amount = self._parse_item_name()
        except Exception as e:
            print(e)
            return False

        user_credits = self._server.execute(Request.Type.GET_CREDITS).data
        price = self._server.execute(
            Request.Type.GET_ITEM,
            item_name
        ).data.buying_price
        if price*amount > user_credits:
            print("Not enough money")
            return False

        return self._confirm_action(
            f"Buy {amount} of {item_name} for {price*amount} credits?"
        )

    def _sell_item(self):
        """Check if user can and wish to sell last item."""
        try:
            item_name, amount = self._parse_item_name()
        except Exception as e:
            print(e)
            return False

        user_has = self._server.execute(
            Request.Type.USER_HAS,
            item_name
        ).data
        if user_has < amount:
            print(f"You don't have {amount} {item_name}")
            return False

        price = self._server.execute(
            Request.Type.GET_ITEM,
            item_name
        ).data.selling_price
        return self._confirm_action(
            f"Sell {amount} of {item_name} for {price*amount} credits?"
        )

    def _parse_item_name(self):
        """Parse item name and amount from last_item.

        Check a lot of stuff and can raise an exeption.
        """
        if not self._last_item:
            raise Exception("No item")

        if self._server.execute(
            Request.Type.ITEM_EXISTS,
            self._last_item
        ).data:
            self._last_item = (self.last_item, 1)
            return self.last_item

        if ' ' not in self.last_item:
            raise Exception(f"No such item: {self._last_item}")

        amount, item_name = self._last_item[::-1].split(' ', 1)
        item_name = item_name[::-1]
        amount = (amount[::-1])
        if not amount.isdigit():
            raise Exception(f"Can't buy or sell {amount} items")

        if not self._server.execute(
            Request.Type.ITEM_EXISTS,
            item_name
        ).data:
            raise Exception(f"No such item: {item_name}")

        self._last_item = (item_name, int(amount))
        return self.last_item

# Output methods

    def show_result(self, response):
        """Show response from server."""
        self._result_retrievers[response.request_type](response)

    def _show_log_in_result(self, response):
        if response.success:
            print("User logged in")
            response = self._server.execute(Request.Type.GET_CREDITS)
            print("You have", response.data, "credits")

        else:
            print(response.message)

    def _show_response(self, response):
        if response.success:
            print(response.data)
        else:
            print(response.message)

    def _show_account(self, response):
        if response.success:
            print("Your account:", response.data)
        else:
            print(response.message)

    def _show_deal_result(self, response):
        if response.success:
            print("Success!")
        else:
            print(response.message)

    def _print_list(self, response):
        if not response.success:
            print(response.message)
        elif not response.data:
            print("Empty")
        else:
            for item in response.data:
                print(item)

    def _print_dict(self, response):
        if not response.success:
            print(response.message)
        elif not response.data:
            print("Empty")
        else:
            for key, val in response.data.items():
                print(key, ": ", val)
