############### Imports and globals ##############
import socket
import sys

import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s: %(message)s',)
logger = logging.getLogger('client')
HOST = ''
PORT = 8888
##################################################

# Connecting to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger.debug('connecting to server')
s.connect((HOST,PORT))
logger.debug('connected')
# main loop
try:
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug('connecting to server')
        s.connect((HOST,PORT))
        # send the data
        message = raw_input('---> ')
        print(message)
        if message == 'quit': break
        logger.debug('sending data: %s', message)
        len_sent = s.send(message)
        #receive respond
        logger.debug('waiting for response')
        response = s.recv(1024)
        logger.debug('response from server: "%s"', response)
        s.close()
finally:
    # clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')
