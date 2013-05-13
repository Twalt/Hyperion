'''
Created on May 12, 2013

@author: Arjun
'''
import sys
import socket
import re

HOST = "irc.snoonet.org"
PORT = 6667
def main(argv=sys.argv):
    NICK = "Twaltbot"
    IDENT = "Twaltbot"
    REALNAME = "Twaltbot"
    readbuffer = ""
    connect = 0
    
    if len(argv) == 3:
        HOST = gethost(sys.argv)
        PORT = getport(sys.argv)
            
    sock = socket.socket();
    sock.connect((HOST, PORT))
    data = "NICK %s\r\n" % NICK
    sock.send(data.encode())
    data = "USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME)
    sock.send(data.encode())
    data = "JOIN #testlab8thing, \r\n"
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
                sock.send(pong.encode())
            if len(line) == 4:
                if line[1]=='PRIVMSG' and line[3] == ':$help':
                    f = open("hello.txt", "r")
                    lineslist = f.readlines();
                    for words in lineslist:
                        output = "PRIVMSG %s :%s\r\n" % (line[2], words)
                        sock.send(output.encode())
            if len(line) == 5:         
                if line[1]=='PRIVMSG' and line[3] == ':$mathify':
                    evalthis = line[4]
                    validMath(evalthis)
                    evalthis = eval(evalthis)
                    output = "PRIVMSG %s :%i\r\n" % (line[2], evalthis)
                    sock.send(output.encode())

def gethost(argv):
    if argv[1].isdigit():
        if "." in argv[2]:
            HOST = argv[2]
    elif argv[2].isdigit():
        if "." in argv[1]:
            HOST = argv[1]
    return HOST

def getport(argv):
    if argv[1].isdigit():
        if "." in argv[2]:
            PORT = int(argv[1])
    elif argv[2].isdigit():
        if "." in argv[1]:
            PORT = int(argv[2])
    return PORT
    
def validMath(arg):
    numlist = re.split('[-/*+]+', arg)
    charlist = re.split('[0123456789]+', arg)
    for val in numlist:
        
    print(1)
    print(numlist)
    print(2)
                    
main()
