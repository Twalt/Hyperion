'''
Created on May 12, 2013

@author: Arjun
'''
import sys
import socket
import string
import urllib

NICK = "shankerabot"
IDENT = "Twaltbot"
REALNAME = "Twaltbot"
readbuffer = ""

if len(sys.argv) == 2:
    if isinstance(sys.argv[0], int):
        if "." in sys.argv[1]:
            HOST = sys.argv[1]
            PORT = sys.argv[0]
    elif isinstance(sys.argv[1], int):
        if "." in sys.argv[0]:
            HOST = sys.argv[0]
            PORT = sys.argv[1]
else:        
    HOST = "irc.snoonet.org"
    PORT = 6667
    
sock = socket.socket();
sock.connect((HOST, PORT))
data = "NICK %s\r\n" % NICK
sock.send(data.encode())
data = "USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME)
sock.send(data.encode())
data = "JOIN #shankeratest, \r\n"
sock.send(data.encode())

while 1:
    sock.recv(1024)