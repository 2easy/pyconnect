#!/usr/bin/env python
############### Imports and globals ##############
import socket
import sys
from request import Request
from protocol import *

import sqlite3
usr_db = sqlite3.connect('usr.sqlite')
c = usr_db.cursor()
try:
    c.execute('create Table Users (User_id int, Pass text)')
except sqlite3.OperationalError: pass
usr_db.commit()

import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s: %(message)s',)
logger = logging.getLogger('client')
HOST = ''
PORT = 8888
##################################################
class UserClient():
    def __init__(self, password = "", usr_id = 0):
        self.usr_id = usr_id
        self.password = password
    def request_server_create(self):
        msg = Request(0,0,CREATE_USER,self.password)
        # send create request to the server
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST,PORT))
            s.send(msg.to_s())
            resp = Request(*s.recv(1024).strip().split(','))
            s.shutdown(socket.SHUT_WR)
            s.close()
        except: return False
        # validate server respond
        if resp.req_type == CREATE_USER:
            self.usr_id = resp.dst_id
            return True
        else: return False
    def save_to_db(self):
        # TODO remembering password
        if self.usr_id == -1: return False
        try:
            c.execute('insert into Users values (?,?)',
                    (self.usr_id,self.password))
            usr_db.commit()
        except: return False
        # if everything went well...
        return True
# new implementation test
cli = UserClient("mama",0)
if cli.request_server_create():
    cli.save_to_db()
    print "success! your id: " + str(cli.usr_id)
# main loop
#while True:
#    print MENU
#    try:
#        opt = int(input("num: "))
#    except:
#        opt = 0
#    if   opt == 1:
#        while True:
#            password = raw_input("Password: ")
#            confirm  = raw_input("Confirm : ")
#            if password == confirm: break
#            else: print "Misstyped, try again."
#        msg = Request(0,0,CREATE_USER,password)
#    elif opt == 5:
#        msg = Request(0,0,LOGOUT)
#    else:
#        message = raw_input('---> ')
#        msg = Request(0,1,FORWARD,message)
#
#    #connect to the server
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect((HOST,PORT))
#    #logger.debug('sending data: %s', message)
#    #print msg.to_s()
#
#    #len_sent = s.send(msg.to_s())
#    s.send(msg.to_s())
#    resp = Request(*s.recv(1024).strip().split(','))
#    if resp.req_type == CREATE_USER:
#        print "resp.dst_id: " + str(resp.dst_id)
#        c.execute('insert into Users values (?,"")', (resp.dst_id,))
#        usr_db.commit()
#        #for us in c.execute('select * from Users'):
#        #    print us
#        print resp.msg
#        print "Your ID is " + resp.dst_id
#    elif resp.req_type == INVALID:
#        print resp.msg
#    s.shutdown(socket.SHUT_WR)
#    s.close()
#    if opt == 5: break
