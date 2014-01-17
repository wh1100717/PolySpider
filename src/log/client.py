###############################################################################
##
##  Copyright (C) 2011-2013 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################
from sh import tail
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import Queue
import threading
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, \
                                       WebSocketClientProtocol, \
                                       connectWS

logQueue = Queue.Queue(maxsize = 100)

class BroadcastClientProtocol(WebSocketClientProtocol):
    """
    Simple client that connects to a WebSocket server, send a HELLO
    message every 2 seconds and print everything it receives.
    """

    def sendLog(self):
        str = ""
        while not logQueue.empty():
            str += logQueue.get()
        if str != "":
            self.sendMessage(str.encode('utf8'))
        reactor.callLater(1, self.sendLog)
    
    def onOpen(self):
        self.sendLog()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {}".format(payload.decode('utf8')))
            
def readLog():
    for line in tail("-f", "/home/eric/project/PolySpider/src/tmp/log/baidu_std.log", _iter=True):
        print line
        logQueue.put(line)
        #self.sendMessage(line)


if __name__ == '__main__':

#   if len(sys.argv) < 2:
#      print("Need the WebSocket server address, i.e. ws://localhost:9000")
#      sys.exit(1)

   factory = WebSocketClientFactory('ws://localhost:9002')
   factory.protocol = BroadcastClientProtocol
   connectWS(factory)
   threading.Thread(target=readLog).start()
   reactor.run()
