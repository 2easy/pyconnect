#!/usr/bin/env python
############### Imports and globals #################
from server_db import ServerDBAgent
db = ServerDBAgent('users.sqlite', ['create table users (pass text)'])

PORT = 8888
from message import *
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
    def __forward_message(self,msg):
        # check sender identity
        try: sender    = self.factory.clients[msg.src_id]
        except KeyError: self.transport.loseConnection()
        if sender != self: self.transport.loseConnection()
        # check if the recipient is logged in
        try: recipient = self.factory.clients[msg.dst_id]
        except KeyError: return
        # forward message
        msg = Message(Message.private,msg.src_id,msg.msg,msg.dst_id)
        recipient.transport.write(str(msg))
    def __login_user(self, req): pass
    def __logout_user(self, req):
        pass
        #logger.debug("Client -- %s -- logged out", self.transport.getPeer())
        #self.factory.clients.remove(self)
        #resp = Message(SERVER_ID, req.src_id, LOGOUT, locale.Login.success)
        #self.transport.write(resp.to_s())
        #self.transport.loseConnection()
    def __create_user(self, req): pass
    def lineReceived(self, line):
        logger.debug("Received: %s   | from %s",
                      repr(line), self.transport.getPeer())
        # parse received packet
        try:    req = Message(*line.split(','))
        except TypeError, msg:
            raise MessageFormatInvalid("Invalid message format: "+msg)
        # react accordingly
        if req.msg_type == Message.private:
            self.__forward_message(req)
        elif req.msg_type == LOGIN:
            self.__login_user(req)
        elif req.msg_type == LOGOUT:
            self.__logout_user(req):
        elif req.msg_type == CREATE_USER:
            self.__create_user(req)
class IMServerFactory(protocol.ServerFactory):
    clients  = {}
    protocol = IMProtocol

if __name__ == '__main__':
    reactor.listenTCP(PORT,IMServerFactory())
    reactor.run()
