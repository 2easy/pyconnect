#!/usr/bin/env python
############### Imports and globals ##############
from server_db import ServerDBAgent
db = ServerDBAgent('users.sqlite', ['create table users (pass text)'])

from sys import exit

import SocketServer
from socket import SHUT_RDWR
from request import Request
from proto_consts import *
import locale

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s')
logger = logging.getLogger('client')
HOST = ''
##################################################
class RequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_addr, server):
        self.logger = logging.getLogger("RequestHandler")
        SocketServer.BaseRequestHandler.__init__(self, request,
                                                 client_addr,
                                                 server)

    def handle(self):
        # receive the data
        self.data = self.request.recv(1024).strip().split(',')
        self.logger.debug("received msg: %s", self.data)
        req = Request(*self.data)
        # process request
        if req.req_type == FORWARD:
            self.request.send(str(req.req_type))
        elif req.req_type == LOGIN:
            #self.request.send(str(req.req_type))
            # TODO do NOT store cleartext passwords
            if self.valid_password(req.src_id,req.msg):
                if req.src_id not in PyConnectServer.logged_users:
                    PyConnectServer.logged_users.append(req.src_id)
                self.logger.debug(PyConnectServer.logged_users)
                self.logger.debug("user %s logged in", req.src_id)
                resp = Request(SERVER_ID,req.src_id,LOGIN,locale.Login.succ)
            else:
                self.logger.debug("user %s FAILED to log in", req.src_id)
                resp = Request(SERVER_ID,req.src_id,INVALID,locale.Login.failed)
            self.request.send(resp.to_s())
        elif req.req_type == LOGOUT:
            self.request.send(str(req.req_type))
        elif req.req_type == CREATE_USER:
            # try creating a user
            usr_id = self.create_user(req.msg)
            if usr_id > 0:
                resp = Request(SERVER_ID,usr_id,CREATE_USER,locale.Rgst.succ)
            else:
                resp = Request(SERVER_ID,0,INVALID,locale.Rgst.failed)
            self.request.send(resp.to_s())
            #for us in c.execute('select * from Users'):
            #    self.logger.debug("%s",us)
        elif req.req_type == DELETE_USER:
            self.request.send(str(req.req_type))
        elif req.not_valid():
            self.logger.debug("received invalid request - dropped")
            return
    def create_user(self, password):
        if password == '': return -1
        else: return db.save_user(password)
    def valid_password(self, uid, password):
        saved_pass = db.fetch_password(uid)
        #self.logger.debug(str(saved_pass))
        if saved_pass != password: return False
        else: return True

class PyConnectServer(SocketServer.TCPServer):
    logged_users = []
    def __init__(self,server_address,handler_class = RequestHandler):
        self.logger = logging.getLogger("PyConnectServer")
        SocketServer.TCPServer.__init__(self,server_address,handler_class)
    #def verify_request(self, request, client_address):
    #    self.logger.debug("received %s from %s",request, client_address)
#        return SocketServer.TCPServer.verify_request(self, request, client_address)
    #    return True

if __name__ == '__main__':
    server = None
    try:
        server = PyConnectServer((HOST,PORT), RequestHandler)
        print "[+] Started pyconnect server"
        server.serve_forever()
    except BaseException as x:
        print x
    except KeyboardInterrupt:
        print "\n[+] Keyboard interrupt, shutting down"
    finally:
        if server:
            server.socket.shutdown(SHUT_RDWR)
            server.socket.close()
