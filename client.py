import socket
import sys
import logging

logging.basicConfig(level=logging.DEBUG,format='%(name)s: %(message)s',)

logger = logging.getLogger('client')
logger.debug('creating socket')

ip, port = ("localhost",8888)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger.debug('connecting to server')
s.connect((ip,port))

# send the data
message = 'hello server'
logger.debug('sending data: %s', message)
len_sent = s.send(message)
#receive respond
logger.debug('waiting for response')
response = s.recv(len_sent)
logger.debug('response from server: "%s"', response)
#clean up
logger.debug('closing socket')
s.close()
logger.debug('done')
