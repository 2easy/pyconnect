#!/usr/bin/env python
############### Imports and globals ##############
import SocketServer
from request import Request

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
        # Echo back to the client
        self.data = self.request.recv(1024).strip().split(',')
        if len(self.data) < 4: return
        self.logger.debug("received msg: %s", self.data)
        req = Request(self.data[0],self.data[1],self.data[2], self.data[3])
        self.request.send(req.msg)

if __name__ == '__main__':
    try:
        server = SocketServer.TCPServer((HOST,PORT), InstantMessageHandler)
        print "[+] Started pyconnect server"
        server.serve_forever()
    except: pass
    finally:
        print "\n[+] Keyboard interrupt, shutting down"
        server.socket.close()
