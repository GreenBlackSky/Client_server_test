"""Text User Interface."""


class TUI:
    """TUI is used to pass information between app and user.

    It can be replaced by any other UI class,
    which implements necessary methods.
    """

    def greet(self):
        """Print welcome messange."""
        print("Welcome!")
        self.help()
        print("Enjoy the game!")

    def help(self):
        """Print tips."""
        print("Tips:\nh - help\nq - quit")

    def farewell(self):
        """Print farewell message."""
        print("Thank you for playing!")

    def say_wait_for_connection(self):
        """Print message about establishing connection."""
        print("connecting...")

    def say_got_connection(self):
        """Inform user about successfully established connection."""
        print("Connected!")

    def ask_retry_connection(self):
        """Inform user about failed connection and ask retry."""
        pass

    def ask_user_name(self):
        pass

    def confirm_user_name(self, user_name):
        pass

    def get_command(self):
        pass

    def show_credits(self, credits_sum):
        pass

    def show_my_items(self, items):
        pass

    def show_all_items(self, items):
        pass

    def confirm_log_out(self):
        pass

