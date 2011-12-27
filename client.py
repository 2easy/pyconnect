#!/usr/bin/env python
############### Imports and globals ##############
import socket
import sys
from request import Request
from protocol import *

import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s: %(message)s',)
logger = logging.getLogger('client')
HOST = ''
PORT = 8888
MENU = '1. create user\n2. login\n3. logout\n4. send message\n5. quit'
##################################################
# main loop
while True:
    print MENU
    try:
        opt = int(input("num: "))
    except:
        opt = 0
    if   opt == 1:
        msg = Request(0,0,CREATE_USER)
    elif opt == 5:
        msg = Request(0,0,LOGOUT)
    else:
        message = raw_input('---> ')
        msg = Request(0,1,FORWARD,message)

    #connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    #logger.debug('sending data: %s', message)
    #print msg.to_s()

    #len_sent = s.send(msg.to_s())
    s.send(msg.to_s())
    response = s.recv(1024)
    #print 'server response ' + response
    #j = raw_input()
    s.shutdown(socket.SHUT_WR)
    s.close()
    if opt == 5: break
