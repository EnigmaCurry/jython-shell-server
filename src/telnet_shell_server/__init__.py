#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ryan McGuire (ryan@enigmacurry.com)"
__date__   = "Sun Mar  1 14:07:52 2009"

import sys
import SocketServer
from threading import RLock
import code

original_displayhook = sys.displayhook
displayhook_lock = RLock()

#This holds the next TelnetConsole's local_vars.
#I know, this is very non-thread safe, I could Lock it,
#but how else do I pass it???
next_local_vars = None

class TelnetConsole(code.InteractiveConsole):
    def __init__(self, request, local_vars=None):
        self.request = request
        if local_vars != None:
            code.InteractiveConsole.__init__(self, local_vars)
        else:
            code.InteractiveConsole.__init__(self)
    def raw_input(self, prompt):
        self.request.send(prompt)
        data = self.request.recv(999999).rstrip()
        return data
    def write(self, data):
        self.request.send(str(data))
    def write_nl(self, data):
        self.write(str(data)+"\r\n")

class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
                                    
class Handler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
    def handle(self):
        console = TelnetConsole(self.request, local_vars=next_local_vars)
        #THIS IS NOT THREADSAFE!!
        #If you telnet in a second time, you'll receive the first sessions's
        #respones. First attempt at locking this failed, so leaving
        #non-threadsafe for now.
        sys.displayhook = console.write_nl
        console.interact()
        self.request.close()
    def finish(self):
        pass
   
def run_server(port, local_vars=None):
    global next_local_vars
    next_local_vars = local_vars
    server = Server(('',port),Handler)
    print "ShellServer started on port "+str(port)
    server.serve_forever()

    
