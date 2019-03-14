# Simple application with client-server architechture

## Client
Simple console app, which allows to communicate with server. User can:
* login into his account, or create new one
* check his credits
* check his items
* check list of all items in game
* purchase items from list, using his credits, or sell any of his items

## Server
Simple net server app. It is used to handle connection with client, provide it with information abot user account and accessible items. Also it gets purchase requests and allows or forbide them. Two data bases are used on server-side. One for items and other for users.

## Dependecies
* Project has been developed with use of python 3.6
* Standart mofule `json` is used to read configuration both for server and for client. 
* Standart module `socket` is used for communication between server and client.
* Both databases are implemented as sqlite db, so `sqlite3` is used to handle them.
* Not a dependancy, but worth mentioning. `server.py` and `client.py` are both meant to be executed from project root. If you want to run any of them from another place, you would want to pass it path to config through argument. Also, a dirty little trick has been used to include shared modules. I didn't want to mess with `PYTHONPATH` or install my packages into system.

## Components
#### Client-side
* Tui - text user interface. Class passes messages from user to ClientCore and vice-versa.
* ClientCore class contains all client-side logic.
#### Server-side
* ConnectionHandler class handles new connections with clients.
* DBHandler class handles data bases.
* ClientHandler class handles client. Contains server-side logic of application.
#### Shared
* Net class is used to maintain connection between client and server.
* ConfigHandler is used to open, parse and check configuration.
* commands module represents... commands! Commands, that user gives to client.

Although, these components are quite naive, they are designed to be replaceble. Query-handling in ClientHandler can be improved by using Celery.
Sqlite as database, TUI as user interface, TCP for networking - any of this components can be replaced by more mature solution.