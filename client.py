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
    def lineReceived(self, line):


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
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST,PORT))
    def disconnect(self):
        if self.s is None:
            return False
        else:
            self.s.shutdown(socket.SHUT_WR)
            self.s.close()
            self.s = None
            return True
    def get_response(self):
        resp_t = self.s.recv(1024).strip().split(',')
        return Request(*resp_t[0:4])
    def request_server_create(self):
        create_msg = Request(0,0,CREATE_USER,self.password)
        # send create request to the server
        self.connect()
        self.s.send(create_msg.to_s())
        resp = self.get_response()
        self.disconnect()
        # validate server respond
        if resp.req_type == CREATE_USER:
            self.usr_id = resp.dst_id
            return True
        else: return False
    def login(self):
        login_msg = Request(self.usr_id, SERVER_ID, LOGIN, self.password)
        self.connect()
        self.s.send(login_msg.to_s())
        resp = self.get_response()
        # validate server respond
        if resp and resp.req_type == LOGIN:
            self.logged_in = True
            return True
        else: return False
    def save_to_db(self,save_pass):
        if self.usr_id == -1: return False
        if save_pass:
            return db.save_user(self.alias,self.usr_id,self.password)
        else:
            return db.save_user(self.alias,self.usr_id,'')
    @classmethod
    def fetch_all(self):
        return db.fetch_all()
