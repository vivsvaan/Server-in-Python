# server.py
import logging

from server.helper.enums import ClientStatus
from server.helper.services import ClientService
from server.helper.utils import read_conf

logging.getLogger()
logging.basicConfig(filename='server_logs.txt', level=logging.DEBUG)

logging.info('---------- STARTING SERVER ----------')
print('---------- STARTING SERVER ----------')

config = read_conf('server.conf')

client_service = ClientService(config.server_host, config.server_port)

client_service.start_server()

try:
    while True:
        """
        While loop to keep listening and accept new connections if no client is connected
        """
        logging.info('Server is Listening...')

        client_service.client, client_service.client_address = client_service.soc.accept()  # accept a new connection

        logging.info('Connected to Client at: {}'.format(client_service.client_address))

        while True:
            """
            While loop to keep reading and processing messages from client
            """
            message = client_service.read_message()
            if not message:
                continue
            if message == ClientStatus.disconnected.value:
                break
            if message == ClientStatus.connected.value:
                connected = True
                continue

            # process message data and return response
            client_service.send_custom_response(message)

        logging.info('Client Disconnected')
        client_service.client.close()
        client_service.client = None
        client_service.client_address = None
        client_service.heartbeat_timestamp = 0
        connected = False

except Exception as e:
    logging.error(e)

logging.info('---------- SERVER STOPPED ----------')
print('---------- SERVER STOPPED ----------')


