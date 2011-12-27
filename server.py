#!/usr/bin/env python
############### Imports and globals ##############
import SocketServer
from request import Request
from protocol import *

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s')
logger = logging.getLogger('client')
HOST = ''
PORT = 8888
##################################################
class InstantMessageHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_addr, server):
        self.logger = logging.getLogger("EchoRequestHandler")
        SocketServer.BaseRequestHandler.__init__(self, request,
                                                 client_addr,
                                                 server)

    def handle(self):
        # receive the data
        self.data = self.request.recv(1024).strip().split(',')
        self.logger.debug("received msg: %s", self.data)
        req = Request(*self.data)
        print req.to_s()
        # process request
        if req.req_type == FORWARD:
            self.request.send(str(req.req_type))
        elif req.req_type == LOGIN:
            self.request.send(str(req.req_type))
        elif req.req_type == LOGOUT:
            self.request.send(str(req.req_type))
        elif req.req_type == CREATE_USER:
            self.request.send(str(req.req_type))
        elif req.req_type == DELETE_USER:
            self.request.send(str(req.req_type))
        elif req.not_valid():
            self.logger.debug("received invalid request - dropped")
            return

if __name__ == '__main__':
    try:
        server = SocketServer.TCPServer((HOST,PORT), InstantMessageHandler)
        print "[+] Started pyconnect server"
        server.serve_forever()
    except: pass
    finally:
        print "\n[+] Keyboard interrupt, shutting down"
        server.socket.close()
