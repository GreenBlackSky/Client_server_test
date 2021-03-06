"""Client application."""

import addshare
from tui import TUI
from clientcore import ClientCore
from serverhandler import ServerHandler
from proxy import Proxy
from confighandler import open_config, transform_config
from signal import signal, SIGINT


def signal_handler(sig, frame):
    """Handle signal and exit."""
    raise SystemExit

signal(SIGINT, signal_handler)


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

    ClientCore(Proxy(ServerHandler(**config)), TUI()).exec()


if __name__ == "__main__":
    run()
