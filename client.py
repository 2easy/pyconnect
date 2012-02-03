#!/usr/bin/env python
############### Imports and globals ##############
import urwid

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.endpoints import TCP4ClientEndpoint
from message import Message

import app_locale

from client_db import ClientDBAgent
db = ClientDBAgent('local_accounts.sqlite',
                   ['create table users (alias text, user_id int, pass text)']
                  )
##################################################
class IMClient(LineReceiver):
    def connectionMade(self):
        self.connected = True
        self.factory.controller.connected()
    def connectionLost(self,reason):
        self.connected = False
        self.factory.controller.disconnected()
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
    def connected(self):
        self.view.rawWrite(app_locale.General.connected)
        self.loop.draw_screen()
    def disconnected(self):
        self.view.rawWrite(app_locale.General.disconnected)
        self.loop.draw_screen()
    def process(self,line):
        msg = Message(*line.split(',',4))
        if msg.msg_type == Message.login and msg.msg == app_locale.Login.succ:
            self.username = msg.dst_id
        self.view.rawWrite(msg.src_id+": "+msg.msg)
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
            elif cmd.startswith('/login'):
                username, password = self.view.footer.edit_text.split(' ',2)[1:3]
                if username and password:
                    msg = str(Message(Message.login,username,password,''))
                    self.connection.transport.write(msg)
                else:
                    self.view.rawWrite("/login <username> <password>")
            elif cmd.startswith('/logout'):
                msg = str(Message(Message.logout,self.username))
                self.connection.transport.write(msg)
            elif cmd.startswith('/create'):
                username, password = self.view.footer.edit_text.split(' ',2)[1:3]
                if username and password:
                    msg = str(Message(Message.create,username,password,''))
                    self.connection.transport.write(msg)
                else:
                    self.view.rawWrite("/create <username> <password>")
            elif cmd.startswith("/msg"):
                try:
                    dst_id, msg = cmd.split(' ',2)[1:]
                except:
                    self.view.rawWrite("/msg <username> <message>")
                    return
                msg = Message(Message.private,self.username,msg,dst_id)
                self.view.rawWrite(msg.src_id+" to "+msg.dst_id+": "+msg.msg)
                self.connection.transport.write(str(msg))
            elif cmd.startswith("/quit"):
                raise urwid.ExitMainLoop()
            self.view.footer.set_edit_text('')
        else: return
        return True

if __name__ == '__main__':
    Controller().main()
