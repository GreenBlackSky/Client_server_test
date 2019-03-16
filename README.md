# Simple application with client-server architechture

## Client
Simple console app, which allows to communicate with server. User can:
* login into his account, or create new one
* check his credits
* check his items
* check list of all items in game
* purchase items from list, using his credits, or sell any of his items

`client.py` is executable for client.

## Server
Simple net server app. It is used to handle connection with client, provide it with information abot user account and accessible items. Also it gets purchase requests and allows or forbide them. Two data bases are used on server-side. One for items and other for users. Config for server must include pathes from project root to both data bases.

`server.py` is executable for server.

## Config
Both client and server must be provided with path to config. Path must be rative from project root. If it is not, application will search for config in default location, which is `{prj}\client\cfg\client_config.json` for client and `{prj}\server\cfg\server_config.json` for server. Config file is in JSON format.

Client config must contain following fields:
* `host` - ip adress of game server
* `port` - port on game server to connect to
* `timeout` - connection timeout

Server config must contain following fields:
* `port` - port to listen to
* `max_init_credits` - lower bound for log in credits
* `min_init_credits` - upper bound for log in credits
* `items_db_path` - relative path to data base with items from project root
* `users_db_path` - relative path to data base with users from project root
* `save_frequency` - frequency of commits to users data base. (In turms of buy/sell operations.)

By default both databases are stored in `{prj}\server\data`

## Dependecies
* Project has been developed with use of python 3.6
* Standart mofule `json` is used to read configuration both for server and for client. 
* Standart module `socket` is used for communication between server and client.
* Both databases are implemented as `json` files. Server config must contain relative pathes to them.
* Not a dependancy, but worth mentioning. `server.py` and `client.py` are both meant to be executed from project root. If you want to run any of them from another place, you would want to pass it path to config through argument. Also, a little trick has been used to include shared modules. I didn't want to mess with `PYTHONPATH` or install my packages into system.

## Components
#### Client-side
* Tui - text user interface. Class passes messages from user to ClientCore and vice-versa.
* ClientCore class contains all client-side logic.
* ServerHandler is TCP based bridge between ClientCore and server.
#### Server-side
* ClientHandler class handles connections with clients. TCP-based.
* ServerCore class contains server-side logic. It takes requests from ClientHandler, processes them and response with answers.
* ServerFabric class produces instances of ServerCore for every new connection.
* ItemsDB and UsersDB handles data bases with items and users respectively. Both JSON-based.
#### Shared
* Request and Answer classe are used to pass information between client and server.
* ConfigHandler is used to open, parse and check configuration.
* User and Item classes represent user and item =).

Although, these components are quite naive, they are designed to be replaceble. Query-handling in ClientHandler can be improved by using Celery.
JSON as database, TUI as user interface, TCP for networking - any of this components can be replaced by more mature solution.