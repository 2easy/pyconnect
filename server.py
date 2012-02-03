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
import app_locale as locale

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s')
logger = logging.getLogger('Server')
######################################################
from twisted.cred import portal, credentials
from auth import *
from twisted.internet import reactor, protocol
from twisted.protocols import basic

class IMProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.peer = self.transport.getPeer()
        self.peer_info = "%s:%s" % (self.peer.host, self.peer.port)
        logger.debug("Client -- %s -- connected", self.peer_info)
    def connectionLost(self, reason):
        logger.debug("Client -- %s -- disconnected", self.peer_info)
    def __forward_message(self,msg):
        # check sender identity
        sender = None
        try: sender    = self.factory.clients[msg.src_id][0]
        except KeyError: self.transport.loseConnection()
        if sender != self:
            self.transport.loseConnection()
            return
        # check if the recipient is logged in
        try: recipient = self.factory.clients[msg.dst_id][0]
        except KeyError: return
        # forward message
        msg = Message(Message.private,msg.src_id,msg.dst_id,msg.msg)
        recipient.transport.write(str(msg))
    def __login_user(self, req):
        creds = credentials.UsernamePassword(req.src_id,req.msg)
        self.factory.portal.login(creds,None,INamedUserAvatar).addCallback(
                self.__login_succeeded).addErrback(self.__login_failed)
    def __login_succeeded(self,avatar_info):
        # add avatar to logged in clients list
        avatar_interface, avatar, logout = avatar_info
        self.factory.clients[avatar.username] = (self,avatar_info)
        self.avatar = avatar
        self.transport.write(str(Message(Message.login,'server',
                                         avatar.username, locale.Login.succ)))
        logger.debug("user %s has logged in", self.avatar.username)
    def __login_failed(self, failure):
        logger.debug("peer %s has failed to log in because of %s",
                     self.peer_info, str(failure.getErrorMessage()))
        self.transport.write(str(Message(Message.login,'server','',
                                         locale.Login.failed)))
        self.transport.loseConnection()
    def __logout_user(self, req):
        try:
            self.factory.clients.pop(self.avatar.username)
            self.transport.write(str(Message(Message.logout,'server',
                                             self.avatar.username,
                                             locale.Logout.succ)))
        finally:
            self.transport.loseConnection()
        logger.debug("user %s has logged out", self.avatar.username)
    def __create_user(self, req):
        # TODO add fullname
        username,password,fullname = req.src_id, req.msg, "noone"
        d = db_agent.find_user(username)
        d.addCallback(self._save_decision,username,password,fullname)
        d.addErrback(self._creation_failure)
    def _save_decision(self,found_user,username,password,fullname):
        if found_user:
            self._creation_failure()
        else:
            d = db_agent.save_user(username,password,fullname)
            d.addCallback(self._creation_success,username,fullname)
            d.addErrback(self._creation_failure)
    def _creation_success(self,result,username,fullname):
        # result arg is always None, but callback must have it
        logger.debug("user %s(%s) has been created", username,fullname)
        self.transport.write(str(Message(Message.create,'server','',
                                         locale.Create.succ)))
    def _creation_failure(self,failure = None):
        if failure: logger.debug(failure.getErrorMessage())
        else: logger.debug("%s requested occupied username", self.peer_info)
        self.transport.write(str(Message(Message.create,'server','',
                                         locale.Create.failed)))
    def lineReceived(self, line):
        logger.debug("Received: %s   | from %s", repr(line), self.peer_info)
        # parse received packet
        try:    req = Message(*line.split(',',3))
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
