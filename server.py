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
class RequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_addr, server):
        self.logger = logging.getLogger("RequestHandler")
        SocketServer.BaseRequestHandler.__init__(self, request,
                                                 client_addr,
                                                 server)

    def handle(self):
        # receive the data
        self.data = self.request.recv(1024).strip().split(',')
        self.logger.debug("received msg: %s", self.data)
        req = Request(*self.data)
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

class PyConnectServer(SocketServer.TCPServer):
    def __init__(self,server_address,handler_class = RequestHandler):
        self.logger = logging.getLogger("PyConnectServer")
        SocketServer.TCPServer.__init__(self,server_address,handler_class)
    #def verify_request(self, request, client_address):
    #    self.logger.debug("received %s from %s",request, client_address)
#        return SocketServer.TCPServer.verify_request(self, request, client_address)
    #    return True

if __name__ == '__main__':
    server = None
    try:
        server = PyConnectServer((HOST,PORT), RequestHandler)
        print "[+] Started pyconnect server"
        server.serve_forever()
    except BaseException as x:
        print x
    except KeyboardInterrupt:
        print "\n[+] Keyboard interrupt, shutting down"
    finally:
        if server: server.socket.close()
