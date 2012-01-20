#!/usr/bin/env python
############### Imports and globals #################
from server_db import ServerDBAgent
db = ServerDBAgent('users.sqlite', ['create table users (pass text)'])

from sys import exit

from request import Request
from proto_consts import *
import locale

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s')
logger = logging.getLogger('Server')
######################################################
from twisted.internet import reactor, protocol
from twisted.protocols import basic

class IMProtocol(basic.LineReceiver):
    def connectionMade(self):
        logger.debug("Client -- %s -- connected", self.transport.getPeer())
    def connectionLost(self, reason):
        logger.debug("Client -- %s -- disconnected", self.transport.getPeer())
    def lineReceived(self, line):
        logger.debug("Received: %s   | from %s",
                      repr(line), self.transport.getPeer())
        req = Request(*line.split(',')[0:4])
        if req.req_type == FORWARD:
            for c in self.factory.clients:
                if c != self: c.transport.write(line+'\n')
        elif req.req_type == LOGIN:
            logger.debug("Client -- %s -- logged in", self.transport.getPeer())
            self.factory.clients.append(self)
            resp = Request(SERVER_ID, req.src_id, LOGIN, locale.Login.success)
            self.transport.write(resp.to_s())
        elif req.req_type == LOGOUT:
            logger.debug("Client -- %s -- logged out", self.transport.getPeer())
            self.factory.clients.remove(self)
            resp = Request(SERVER_ID, req.src_id, LOGOUT, locale.Login.success)
            self.transport.write(resp.to_s())
            self.transport.loseConnection()
        elif req.req_type == CREATE_USER:
            # TODO
            pass
        if line == 'quit':
            self.sendLine("Goodbye.")
            self.transport.loseConnection()
            return

class IMServerFactory(protocol.ServerFactory):
    clients  = []
    protocol = IMProtocol

if __name__ == '__main__':
    reactor.listenTCP(PORT,IMServerFactory())
    reactor.run()
