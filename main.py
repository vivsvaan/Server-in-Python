# main.py

from server.manager import ServerManager
from client.manager import ClientManager

ServerManager().start()
ClientManager.start()