"""Server application."""

import addshare
from confighandler import open_config, transform_config
from dbhandler import DBHandler
from netserver import NetworkServer
from connectionhandler import ConnectionHandler
from clienthandler import ClientHandlerFabric


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

    network_server = NetworkServer(config["port"])
    items_db = DBHandler(config["items_db_path"])
    users_db = DBHandler(config["users_db_path"])
    client_handler_fabric = ClientHandlerFabric(users_db, items_db)
    ConnectionHandler(network_server, client_handler_fabric).exec()

if __name__ == "__main__":
    run()

# TODO handle interraptions
