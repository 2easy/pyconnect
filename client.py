#!/usr/bin/env python
############### Imports and globals ##############
import sys, socket
from request import Request

from cli_db import ClientDBAgent
db = ClientDBAgent('cli_db.sqlite',
                   ['create table users (alias text, user_id int, pass text)']
                  )
from proto_consts import *
##################################################
class UserClient(object):
    def __init__(self, password = '', usr_id = 0, alias = 'noone'):
        self.password = password
        self.usr_id   = int(usr_id)
        self.alias    = alias

    def send(self,msg):
        #try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        s.send(msg.to_s())
        resp_t = s.recv(1024).strip().split(',')
        resp = Request(*resp_t[0:4])
        s.shutdown(socket.SHUT_WR)
        s.close()
        return resp
        #except: return None
    def request_server_create(self):
        msg = Request(0,0,CREATE_USER,self.password)
        # send create request to the server
        resp = self.send(msg)
        # validate server respond
        if resp.req_type == CREATE_USER:
            self.usr_id = resp.dst_id
            return True
        else: return False
    def login(self):
        msg = Request(self.usr_id, SERVER_ID, LOGIN, self.password)
        resp = self.send(msg)
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
