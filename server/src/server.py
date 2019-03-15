"""Server application."""

import addshare
from confighandler import open_config, transform_config
from item_db import ItemsDB
from user_db import UsersDB
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

    try:
        users_db = UsersDB(config["users_db_path"])
    except OSError:
        print("Unable to open users data base")
        return
    except ValueError:
        print("Unable to read users data base")
        return

    try:
        items_db = ItemsDB(config["items_db_path"])
    except OSError:
        print("Unable to open users data base")
        return
    except ValueError:
        print("Unable to read users data base")
        return

    ClientHandler.set_db(items_db, users_db)
    ClientHandler.set_limits(config["min_init_credits"],
                             config["max_init_credits"])
    NetworkServer(config["port"], ClientHandler).exec()

if __name__ == "__main__":
    run()

# TODO handle interraptions
