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
logger = logging.getLogger('client')
HOST = ''
######################################################
from twisted.internet import reactor, protocol
from twisted.protocols import basic

class IMProtocol(basic.LineReceiver):
    def connectionMade(self):
        print "Client connected"
        self.factory.clients.append(self)
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
    def lineReceived(self, line):
        print "received",repr(line)
        print str(self.factory.clients)
        if line == 'quit':
            self.sendLine("Goodbye.")
            self.transport.loseConnection()
            return
        for c in self.factory.clients:
            c.transport.write(line+'\n')

class IMServerFactory(protocol.ServerFactory):
    clients  = []
    protocol = IMProtocol

if __name__ == '__main__':
    reactor.listenTCP(PORT,IMServerFactory())
    reactor.run()
#if __name__ == '__main__':
#    server = None
#    try:
#        server = PyConnectServer((HOST,PORT), RequestHandler)
#        print "[+] Started pyconnect server"
#        server.serve_forever()
#    except BaseException as x:
#        print x
#    except KeyboardInterrupt:
#        print "\n[+] Keyboard interrupt, shutting down"
#    finally:
#        if server:
#            server.socket.shutdown(SHUT_RDWR)
#            server.socket.close()
