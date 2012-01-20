#!/usr/bin/env python
from twisted.internet import stdio, reactor, protocol
from twisted.protocols import basic

import re

class DataForwardingProtocol(protocol.Protocol):
    def __init__(self):
        self.output = None
        self.normalizeNewlines = False
    def dataReceived(self, data):
        if self.normalizeNewlines:
            data = re.sub(r"(\r\n|\n)", "\r\n", data)
        if self.output:
            self.output.write(data)

class StdioProxyProtocol(DataForwardingProtocol):
    def connectionMade(self):
        inputForwarder = DataForwardingProtocol()
        inputForwarder.output = self.transport
        inputForwarder.normalizeNewlines = True

        stdioWrapper = stdio.StandardIO(inputForwarder)
        self.output = stdioWrapper
        print "Connected to server. Press ctrl-c to close connection"

class StdioProxyFactory(protocol.ClientFactory):
    protocol = StdioProxyProtocol

    def clientConnectionLost(self, transport, reason):
        reactor.stop()
    def clientConnectionFailed(self, transport, reason):
        print reason.getErrorMessage()
        reactor.stop()

if __name__ == "__main__":
    reactor.connectTCP("127.0.0.1", 8888, StdioProxyFactory())
    reactor.run()
