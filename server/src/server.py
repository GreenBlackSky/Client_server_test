"""Server application."""

import addshare
from confighandler import open_config, transform_config
from dbhandler import UsersDB, ItemsDB
from netserver import NetworkServer
from clienthandler import ClientHandler


def run():
    """Exec loop of server application."""
    config_must_have = {
        "port": int,
        "max_init_credits": int,
        "min_init_credits": int,
        "items_db_path": str,
        "users_db_path": str
    }
    config = open_config("server/cfg/server_config.json")
    if config is None or not transform_config(config, config_must_have):
        return

    users_db = UsersDB(config["users_db_path"])
    items_db = ItemsDB(config["items_db_path"])
    ClientHandler.set_db(users_db, items_db)
    NetworkServer(config["port"], ClientHandler).exec()

if __name__ == "__main__":
    run()

# TODO handle interraptions
