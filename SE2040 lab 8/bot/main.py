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
connect = 0

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
    received = sock.recv(1024)
    readbuffer = readbuffer + received.decode("utf-8")
    temp=readbuffer.split("\n")
    readbuffer=temp.pop( )
    for line in temp:
        line=line.rstrip()
        line=line.split()
        print(line)
        if line[0] == "PING":
            pong = "PONG %s\r\n" % line[1]
            sock.send(pong.encode('utf-8'))
        if len(line) > 4:
            if line[1]=='PRIVMSG' and line[3] == ':shankerabot' and line[4] == 'hello':
                f = open("hello.txt", "r")
                lineslist = f.readlines();
                for words in lineslist:
                    output = "PRIVMSG %s :%s\r\n" % (line[2], words)
                    sock.send(output.encode())
            if line[1]=='PRIVMSG' and line[3] == ':$mathify':
                evalthis = line[4]
                evalthis = eval(evalthis)
                output = "PRIVMSG %s :%i\r\n" % (line[2], evalthis)
                sock.send(output.encode())
