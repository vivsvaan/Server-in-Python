# services.py

import socket
import logging


class TPCService:
    """
    This Service performs all the TCP Socket related tasks
    """

    host = ""
    port = ""
    soc = None

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def connect_to_server(self):
        """
        Connects to the server
        """
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((self.host, self.port))


# class Server




