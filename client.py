#!/usr/bin/env python
############### Imports and globals ##############
import socket
import sys
from request import Request

import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s: %(message)s',)
logger = logging.getLogger('client')
HOST = ''
PORT = 8888
MENU = '1. create user\n2. login\n3. logout\n4. send message\n5. quit'
##################################################
# main loop
try:
    while True:
        #connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        print MENU
        opt = int(input("num: "))
        if   opt == 1:
            msg = Request(0,0,0)
        elif opt == 5: break
        else:
            message = raw_input('---> ')
            msg = Request(0,1,3,message)

        #logger.debug('sending data: %s', message)
        print msg.to_s()

        if opt != 5:
            len_sent = s.send(msg.to_s())
            response = s.recv(1024)
        s.close()
finally:
    # clean up
    logger.debug('closing socket')
    s.close()
    logger.debug('done')
