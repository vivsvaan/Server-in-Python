import socket
import logging
import datetime
import server.helper.utils as utils
from server.helper.consts import (
    NUMBER_OF_SIMULTANEOUS_CLIENTS, DEFAULT_HEARTBEAT_INTERVAL,
    BUFFER_SIZE, HEARTBEAT_INTERVAL_MULTIPLIER
)
from server.helper.enums import (
    MessageRequestType, ClientStatus
)


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

        logging.info("Creating Server")
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.bind((self.host, self.port))  # bind host and port together
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


class ClientService(TCPService):
    """
    Every Communication from/to client must happen through here
    """

    def __init__(self, host, port):
        super().__init__(host, port)
        self.client = None
        self.client_address = None
        self.heartbeat_timestamp = 0
        self.heartbeat_interval = DEFAULT_HEARTBEAT_INTERVAL
        """
        Note - Heartbeat is an empty message which clients sends to the server stating that client is still connected.
        In case client disconnects without telling the server, 
        server will drop that client's connection.
        """

    def start_server(self, clients=1):
        """
        Starts the Python Server
        :param clients: configure how many clients the server can listen to simultaneously
        """

        self.create_server()
        self.start_listening(clients)

    def read_message(self):
        """
        Reads the message received from Client
        :return: False (if message is null or Heartbeat)
        :return: ClientStatus (if message is Connect or Disconnect Request)
        :return: else decoded message
        """

        message = self.client.recv(BUFFER_SIZE)
        if not message or message == b'':
            """
            If timestamp of last heartbeat is older that heartbeat interval, drop the connection
            """

            if self.heartbeat_timestamp and (
                    self.heartbeat_timestamp < (
                    datetime.datetime.now() - datetime.timedelta(seconds=self.heartbeat_interval))):
                return ClientStatus.disconnedted.value
            return False

        message = utils.deserialize(message)

        if message.msg_type == MessageRequestType.connect.value:
            """
            Update the client heartbeat and send connection response to client
            """

            self.heartbeat_timestamp = datetime.datetime.now()
            self.heartbeat_interval = int(message.heartbeat_interval*HEARTBEAT_INTERVAL_MULTIPLIER)
            self.send_connection_response(is_success=True)
            return ClientStatus.connected.value

        elif message.msg_type == MessageRequestType.disconnect.value:
            return ClientStatus.disconnedted.value

        elif message.msg_type == MessageRequestType.heartbeat.value:
            self.heartbeat_timestamp = datetime.datetime.now()
            return False

        elif message.msg_type == MessageRequestType.message.value:
            self.heartbeat_timestamp = datetime.datetime.now()
            return message

        return False

    def send_message(self, message, serialized=False):
        """
        Send message to the client
        :param message: message to be sent
        :param serialized: message serialization status (True/False)
        """

        data = message
        if not serialized:
            data = utils.serialize(data)
        self.client.send(data)

        logging.info("""
        __________ SENDING DATA TO CLIENT __________
        Message : {message}
        ____________________________________________
        """.format(message=message))

    def send_connection_response(self, is_success=False):
        """
        Send the connection response
        :param is_success: Connection Status (True/False)
        """

        logging.info("Sending Connection Response: ", is_success)
        conn_res = "is_connected: True"
        self.send_message(conn_res)
