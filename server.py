import SocketServer

import logging
logging.basicConfig(level=logging.DEBUG,format='%(name)s: %(message)s',)

class EchoRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_addr, server):
        self.logger = logging.getLogger("EchoRequestHandler")
        SocketServer.BaseRequestHandler.__init__(self, request,
                                                 client_addr,
                                                 server)

    def handle(self):
        # Echo back to the client
        data = self.request.recv(1024)
        self.logger.debug("received msg: %s", data)
        self.request.send(data)

if __name__ == '__main__':
    address = ('localhost', 8888)

    server = SocketServer.TCPServer(address, EchoRequestHandler)

    server.serve_forever()
