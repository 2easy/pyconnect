#!/usr/bin/env python
############### Imports and globals ##############
import urwid

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.endpoints import TCP4ClientEndpoint
from message import Message

from client_db import ClientDBAgent
db = ClientDBAgent('local_accounts.sqlite',
                   ['create table users (alias text, user_id int, pass text)']
                  )
##################################################
class IMClient(LineReceiver):
    def connectionMade(self):
        self.connected = True
    def connectionLost(self,reason):
        self.connected = False
    def lineReceived(self, line):
        self.factory.controller.process(line)

class IMClientFactory(Factory):
    protocol = IMClient

    def __init__(self, controller):
        self.controller = controller

    def buildProtocol(self, addr):
        cli = self.protocol()
        cli.factory = self
        cli.username = self.controller.username
        #self.controller.connection = cli
        return cli
    def clientConnectionLost(self,connector,reason):
        reactor.stop()
    def clientConnectionFailed(self,connector,reason):
        reactor.stop()

class View(object):
    palette = [
            ('body', 'default', 'default'),
            ('footer', 'white', 'dark blue'),
    ]

    def __init__(self):
        self.walker = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.walker)
        self.footer = urwid.Edit("$ ")
        self.frame = urwid.Frame(self._wrap(self.listbox, 'body'),
            footer=self._wrap(self.footer,'footer'),
            focus_part='footer')

    def _wrap(self, widget, attr_map):
        return urwid.AttrMap(widget, attr_map)
    def rawWrite(self, text):
        self.walker.append(urwid.Text(text))
        self.walker.set_focus(len(self.walker.contents))
class Controller(object):
    def __init__(self):
        self.username = "noone"
        self.view = View()
        self.factory = IMClientFactory(self)

    def main(self):
        self.loop = urwid.MainLoop(self.view.frame, self.view.palette,
                                   unhandled_input=self.handleKeys,
                                   event_loop=urwid.TwistedEventLoop())
        self.loop.run()
    def process(self,line):
        msg = Message(*line.split(',',4))
        self.view.rawWrite(msg.msg)
        self.loop.draw_screen()
    def _assignConnection(self,conn):
        self.connection = conn
    def handleKeys(self, key):
        if key == "enter":
            cmd = self.view.footer.edit_text
            if cmd.startswith("/connect"):
                point = TCP4ClientEndpoint(reactor,'localhost',8888)
                d = point.connect(self.factory)
                d.addCallback(self._assignConnection)
            elif cmd.startswith('/disconnect'):
                self.connection.transport.loseConnection()
            elif cmd.startswith("/s"):
                msg_type, src_id, msg, dst_id = cmd[2:].split(',')
                msg = str(Message(msg_type,src_id,msg,dst_id))
                self.connection.transport.write(msg)
            elif cmd.startswith("/quit"):
                raise urwid.ExitMainLoop()
            self.view.footer.set_edit_text('')
        else: return
        return True

if __name__ == '__main__':
    Controller().main()
