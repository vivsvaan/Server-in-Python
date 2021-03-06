# manager.py

import logging

from server.helper.enums import ClientStatus
from server.helper.services import TCPService, MessageProcessingService
from server.helper.interfaces import ClientInterface
from server.helper.utils import read_conf


class ServerManager(TCPService):
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

    def start(self, clients=1):
        """
        Starts the Python Server
        :param clients: configure how many clients the server can listen to simultaneously
        """

        self.create_server()
        self.start_listening(clients)
        is_connected = False

        try:
            while True:
                if not is_connected:
                    logging.info('Waiting for a client to connect...')

                    client, addr = self.soc.accept()  # accept a new connection
                    client_interface = ClientInterface(client, addr)

                    logging.info('Connected to Client at: {}'.format(client_interface.client_address))
                    is_connected = True
                    processing_service = MessageProcessingService(client_interface)
                    processing_service.__enter__()
                elif processing_service.is_terminated:
                    is_connected = False

        except Exception as e:
            logging.error(e)

    logging.info('---------- SERVER STOPPED ----------')
    print('---------- SERVER STOPPED ----------')
