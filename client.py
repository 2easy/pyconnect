#!/usr/bin/env python
############### Imports and globals ##############
from twisted.internet import protocol
import sys, socket
from request import Request

from cli_db import ClientDBAgent
db = ClientDBAgent('cli_db.sqlite',
                   ['create table users (alias text, user_id int, pass text)']
                  )
from proto_consts import *
##################################################
class IMClient(protocol.Protocol):
    def __init__(self, password, usr_id, alias):
        self.password = password
        self.usr_id   = int(usr_id)
        self.alias    = alias
    def connectionMade(self):
        self.connected = True
    def connectionLost(self,connection,reason):
        self.connected = False
    def parse(self,line):
        vals = line.split(',')[0:4]
    def lineReceived(self, line): pass

class IMClientFactory(protocol.ClientFactory):
    protocol = IMClient

    def clientConnectionLost(self,connector,reason):
        reactor.stop()
    def clientConnectionFailed(self,connector,reason):
        reactor.stop()

class UserClient(object):
    def __init__(self, password = '', usr_id = 0, alias = 'noone'):
        self.s = None
        self.password = password
        self.usr_id   = int(usr_id)
        self.alias    = alias

