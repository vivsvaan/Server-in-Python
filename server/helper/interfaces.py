# interfaces.py

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


class ClientInterface:
    """
    Every Communication from/to client must happen through here
    """

    def __init__(self, client, address):
        self.client = client
        self.client_address = address
        self.heartbeat_timestamp = 0
        self.heartbeat_interval = DEFAULT_HEARTBEAT_INTERVAL
        """
        Note - Heartbeat is an empty message which clients sends to the server stating that client is still connected.
        In case client disconnects without notifying the server, 
        server will drop that client's connection using heartbeat.
        """

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

    def send_custom_response(self, message):
        """
        Send the response to client
        :param message: message to be sent
        """

        logging.info("Sending Custom Response: ", message)
        self.send_message(message)
