# server.py

import logging

from server.helper.enums import ClientStatus
from server.helper.services import TCPService
from server.helper.interfaces import ClientInterface
from server.helper.utils import read_conf


class Server(TCPService):
    def __init__(self, host=None, port=None):
        logging.getLogger()
        logging.basicConfig(filename='server_logs.txt', level=logging.DEBUG)

        logging.info('---------- STARTING SERVER ----------')
        print('---------- STARTING SERVER ----------')

        if not (host and port):
            config = read_conf('server.conf')
            host, port = config.host, config.port

        self.host, self.port = host, int(port)
        super().__init__(self.host, self.port)

    def run_server(self, clients=1):
        """
        Starts the Python Server
        :param clients: configure how many clients the server can listen to simultaneously
        """

        self.create_server()
        self.start_listening(clients)

        try:
            while True:
                """
                While loop to keep listening and accept new connections if no client is connected
                """
                logging.info('Server is Listening...')

                client, addr = self.soc.accept()  # accept a new connection

                client_interface = ClientInterface(client, addr)

                logging.info('Connected to Client at: {}'.format(client_interface.client_address))

                while True:
                    """
                    While loop to keep reading and processing messages from client
                    """
                    message = client_interface.read_message()
                    if not message:
                        continue
                    if message == ClientStatus.disconnected.value:
                        break
                    if message == ClientStatus.connected.value:
                        continue

                    # process message data and return response
                    client_interface.send_custom_response(message)

                logging.info('Client Disconnected')
                client_interface.client.close()
                client_interface.client = None
                client_interface.client_address = None
                client_interface.heartbeat_timestamp = 0

        except Exception as e:
            logging.error(e)

    logging.info('---------- SERVER STOPPED ----------')
    print('---------- SERVER STOPPED ----------')
