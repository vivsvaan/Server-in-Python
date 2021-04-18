# client.py
import logging

logging.getLogger()
logging.basicConfig(filename='client_logs.txt', level=logging.DEBUG)

logging.info('---------- STARTING CLIENT ----------')
print('---------- STARTING CLIENT ----------')

config = read_conf('client.conf')

server_service = ServerService(config.server_host, config.server_port)







