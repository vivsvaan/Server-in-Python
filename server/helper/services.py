# services.py
import queue
import socket
import logging
import multiprocessing
from server.helper.consts import (
    NUMBER_OF_SIMULTANEOUS_CLIENTS, READ_QUEUE_SIZE, WRITE_QUEUE_SIZE,
)
from server.helper.enums import ClientStatus


class TCPService:
    """
    This Service performs all the TCP Socket related tasks
    """

    host = ''
    port = ''
    soc = None

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def create_server(self):
        """
        Creates a Server
        """

        logging.info("Creating Server...")
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.bind((self.host, self.port))  # bind host and port together
            logging.info("Server Created")
        except Exception as e:
            logging.error(e)
            raise e

    def start_listening(self, clients=NUMBER_OF_SIMULTANEOUS_CLIENTS):
        """
        Starts Listening for clients
        :param clients: configure how many clients the server can listen to simultaneously
        """

        try:
            self.soc.listen(clients)
            logging.info("Server is Up" +
                         "IP: ", self.host,
                         "Port: ", self.port)
            print("Server is Up" + "IP: ", self.host, "Port: ", self.port)
        except Exception as e:
            logging.error(e)
            raise e
