"""Server application."""

import addshare
from confighandler import open_config, transform_config
from item_json_db import ItemsDB
from user_json_db import UsersDB
from servercore import ServerCore
from clienthandler import ClientHandler


def run():
    """Exec loop of server application."""
    config_must_have = {
        "port": int,
        "max_init_credits": int,
        "min_init_credits": int,
        "save_frequency": int,
        "simultanious_log_ins": bool,
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

    server_core = ServerCore(items_db, users_db,
                             config["min_init_credits"],
                             config["max_init_credits"],
                             config["save_frequency"],
                             config["simultanious_log_ins"])
    ClientHandler(config["port"], server_core).exec()

if __name__ == "__main__":
    run()

# TODO handle interraptions
