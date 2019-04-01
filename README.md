# Simple application with client-server architechture

## Client

Simple console app, which allows to communicate with server. User can:

* get list of existing accounts
* login into his account, or create new one
* check his credits
* check his items
* check list of all items in game
* purchase items from list, using his credits, or sell any of his items
* check how much items of some kind he has
* get prices for item

`client.py` is executable for client.

## Server

Simple net server app. It is used to handle connection with client, provide it with information abot user account and accessible items. Also it gets purchase requests and allows or forbide them. Two data bases are used on server-side. One for items and other for users. Config for server must include pathes from project root to both data bases.

`server.py` is executable for server.

## Config

Both client and server must be provided with path to config. Path must be relative from project root. If it is not, application will search for config in default location, which are `{prj}\client\cfg\client_config.json` and `{prj}\server\cfg\server_config.json` for client and for server respectively. Config file is in JSON format.

Client config must contain following fields:

* `host` - ip adress of game server
* `port` - port on game server to connect to
* `timeout` - connection timeout

Server config must contain following fields:

* `port` - port to listen to
* `max_init_credits` - lower bound for log in credits
* `min_init_credits` - upper bound for log in credits
* `items_db_path` - path to data base with items
* `users_db_path` - path to data base with users
* `save_frequency` - frequency of commits to users data base. (In turms of successfull operations.)
* `simultanious_log_ins` - flag, which allows different clients simultaniously log in into one user. To forbid such behaviour, one must set it to empty string.

## Dependecies

* Project has been developed with use of python 3.6
* Standart mofule `json` is used to read configuration both for server and for client.
* Standart module `socket` is used for communication between server and client.
* Both databases are also implemented as `json` files. Server config must contain relative pathes to them.
* Not a dependancy, but worth mentioning. `server.py` and `client.py` are both meant to be executed from project root. If you want to run any of them from another place, you would want to pass it path to config through argument. Also, a little trick has been used to include shared modules. I didn't want to mess with `PYTHONPATH` or install my packages into system.

## Components

### Client-side

* `Tui` - text user interface. Class passes messages from user to `ClientCore` and vice-versa. It can also interract directly with `ServerHandler`, without changing clients state. But this direct interration MUST be used only for retrieving information.
* `ClientCore` class contains all client-side logic.
* `ServerHandler` is TCP based bridge between `ClientCore` and server. Plain and simple, it can only pass requests and return responses.
* `Proxy` - wrapper for ServerHandler. It has cache and some mechanics to use it in order to reduce number of excessive network communications.

### Server-side

* `ClientHandler` class handles connections with clients. TCP-based.
* `ServerCore` class contains server-side logic. It creates new handler foe each new client connection. Handler takes requests from `ClientHandler`, processes them and response with answers. All Handlers share users and items data bases.
* `ItemsDB` and `UsersDB` handles data bases with items and users respectively. Both JSON-based. `UserDB` rewrites whole JSON-file on commit, which is sad. But JSON was never intended to be used in huge scaled data bases and here serves just as an example. In more serious project one would replace `UserDB` with some SQL or NoSQL data base handler, like Sqlite or PostgreSQL.

### Shared

* `Request` and `Response` classes are used to pass information between client and server.
 There are 18 types of these. Each of them do quite what its name stands for.
    1. USER_EXISTS
    1. GET_USER
    1. GET_ALL_USERS
    1. GET_ALL_USERS_NAMES
    1. GET_ITEM
    1. GET_ALL_ITEMS
    1. GET_ALL_ITEMS_NAMES
    1. GET_CURRENT_USER
    1. GET_CURRENT_USER_NAME
    1. GET_CREDITS
    1. USER_HAS
    1. GET_USER_ITEMS
    1. GET_USER_ITEMS_NAMES
    1. PING
    1. LOG_IN
    1. PURCHASE_ITEM
    1. SELL_ITEM
    1. LOG_OUT

* `ConfigHandler` is used to open, parse and check configuration.
* `User` and `Item` classes represent user and item =).
* `addshared` module contains method `get_abs_path`, which gets absolute path to project directory. On include it modifyes local `PYTHONPATH` (for this run of project) by including `shared` directory.

Although, these components are quite naive, they are designed to be replaceble. Query-handling in `ServerCore` can be improved by using Celery.
JSON as database, TUI as user interface, TCP for networking - any of this components can be replaced by more mature solution.

## Path of request

User asks client app to do something via UI. `TUI` in this case. `TUI` triggers some methods in `ClientCore` mechanism directly, or generates `Request` object and passes in to `Proxy`. `Proxy` processes request, response with cached value if possible or honestly passes request to `ServerHandler`. `ServerHandler` passes it to server app using network. In server app `ClientHandler` gets the request. It has its own instance of `ServerCore._Handler`. Though `ServerCore` contains all server logic inside itself, it generates handlers to deal with multile clients simulteniously. `_Handler` process the request, using `ServerCore` methods and data bases. It generates `Response`, which contains result of request execution.
Then `Response` makes the same way backwards to User.