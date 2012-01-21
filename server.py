#!/usr/bin/env python
############### Imports and globals #################
from server_db import ServerDBAgent
db_agent = ServerDBAgent('users.sqlite',
                         ['''create table users
                                 (username text,
                                  fullname text,
                                  password text)'''])

PORT = 8888
from message import *
import locale

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s')
logger = logging.getLogger('Server')
######################################################
from twisted.cred import portal, credentials
from auth import *
from twisted.internet import reactor, protocol, defer
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
    def __login_user(self, req):
        creds = credentials.UsernamePassword(req.src_id,req.msg)
        self.factory.portal.login(creds,None,INamedUserAvatar).addCallback(
                self.__login_succeeded).addErrback(self.__login_failed)
    def __login_succeeded(self,avatar_info):
        # add avatar to logged in clients list
        avatar_interface, avatar, logout = avatar_info
        self.factory.clients[avatar.username] = avatar_info
        self.transport.write(str(Message(Message.login,0,locale.Login.succ_msg,
                                         avatar.username)))
    def __login_failed(self, failure):
        logger.debug("failure: %s", str(failure))
        self.transport.write(str(Message(Message.login,0,
                                         locale.Login.failed_msg,
                                         0)))
        self.transport.loseConnection()
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
            raise MessageFormatInvalid("Invalid message format: "+str(msg))
        # react accordingly
        if req.msg_type == Message.private:
            self.__forward_message(req)
        elif req.msg_type == Message.login:
            self.__login_user(req)
        elif req.msg_type == Message.logout:
            self.__logout_user(req)
        elif req.msg_type == Message.create:
            self.__create_user(req)
class IMServerFactory(protocol.ServerFactory):
    protocol = IMProtocol
    clients  = {}
    def __init__(self, portal):
        self.portal = portal

if __name__ == '__main__':
    p = portal.Portal(DBRealm(db_agent))
    p.registerChecker(DBPasswordChecker(db_agent))
    reactor.listenTCP(PORT,IMServerFactory(p))
    reactor.run()
