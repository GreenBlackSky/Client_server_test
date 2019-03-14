"""Client application."""

import addshare
from tui import TUI
from clientcore import ClientCore
from serverhandler import ServerHandler
from confighandler import open_config, transform_config


def run():
    """Exec loop of client application."""
    config_must_have = {
        "host": str,
        "port": int,
        "timeout": float
    }
    config = open_config("client/cfg/client_config.json")
    if config is None or not transform_config(config, config_must_have):
        return

    ClientCore(ServerHandler(**config), TUI()).exec()


if __name__ == "__main__":
    run()
