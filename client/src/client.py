"""Client application."""

from shared.confighandler import open_config, transform_config
from tui import TUI
from clientcore import ClientCore
from shared.net import NetworkClient


def run():
    """Exec loop of client application."""
    config_must_have = {
        "server_ip": str,
        "server_port": int,
        "attempts": int,
        "timeout": int
    }
    config = open_config("client/cfg/client_config.json")
    if config is None or not transform_config(config, config_must_have):
        return

    ClientCore(NetworkClient(config**), TUI()).exec()


if __name__ == "__main__":
    run()
