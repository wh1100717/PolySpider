#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys

from sh import tail
import Queue
import threading
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory, \
                                       WebSocketServerProtocol, \
                                       listenWS

logQueue = Queue.Queue(maxsize = 100)

class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
    #         msg = "{} from {}".format(payload.decode('utf8'), self.peer)
            self.factory.broadcast(payload.decode('utf8'))

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug = False, debugCodePaths = False):
        WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
        self.clients = []
        self.sendLog()

    def sendLog(self):
         str = ""
         while not logQueue.empty():
            str += logQueue.get()
         if str != "":
             self.broadcast(str.encode('utf8'))
         reactor.callLater(1, self.sendLog)

    def register(self, client):
        if not client in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            print("message sent to {}".format(c.peer))

def readLog(log_path):
#    for line in tail("-f", "/home/eric/project/PolySpider/src/tmp/log/baidu_std.log", _iter=True):
    for line in tail("-f", log_path, _iter=True):
        print line
        logQueue.put(line)


if __name__ == '__main__':
    '''
    argv[1]为日志绝对路径 必填项
    argv[2]为服务器端口号 默认未9002    
    网页日志服务器启动方式如下：
        python server.py /home/eric/project/PolySpider/src/tmp/log/baidu_std.log 9002 
    '''
    log_path = sys.argv[1]
    if len(sys.argv) < 1:
        print "Need log_path, i.e. python server.py /var/sys.log"
        sys.exit(1)
    elif len(sys.argv) < 2:
        print "No port input, 9002 as default"
        log_path = sys.argv[1]
        port = '9002'
    else:
        log_path = sys.argv[1]
        port = sys.argv[2]

    log.startLogging(sys.stdout)
    debug = True

    ServerFactory = BroadcastServerFactory

    factory = ServerFactory("ws://localhost:" + port,
                            debug = debug,
                            debugCodePaths = debug)

    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions(allowHixie76 = True)
    listenWS(factory)

    webdir = File(".")
    web = Site(webdir)
    threading.Thread(target=readLog, args=(log_path,)).start()
    reactor.listenTCP(8080, web)

    reactor.run()