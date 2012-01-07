#!/usr/bin/env python
############### Imports and globals ##############
import socket
import sys
from request import Request
from proto_consts import *

import sqlite3
usr_db = sqlite3.connect('usr.sqlite')
c = usr_db.cursor()
try:
    c.execute('create Table Users (User_id int, Pass text)')
except sqlite3.OperationalError: pass
usr_db.commit()

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',)
logger = logging.getLogger('client')
HOST = ''
PORT = 8888
##################################################
class UserClient():
    def __init__(self, password = "", usr_id = 0):
        try: self.usr_id = int(usr_id)
        except: return
        self.password = password
    def send(self,msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST,PORT))
            s.send(msg.to_s())
            resp = Request(*s.recv(1024).strip().split(','))
            s.shutdown(socket.SHUT_WR)
            s.close()
            return resp
        except: return None
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
        msg = Request(self.usr_id, SERVER_ID, LOGIN,self.password)
        resp = self.send(msg)
        # validate server respond
        if resp and resp.req_type == LOGIN:
            self.logged_in = True
            return True
        else: return False
    def save_to_db(self):
        # TODO remember password
        if self.usr_id == -1: return False
        try:
            c.execute('insert into Users values (?,?)',
                    (self.usr_id,self.password))
            usr_db.commit()
        except: return False
        # if everything went well...
        return True
