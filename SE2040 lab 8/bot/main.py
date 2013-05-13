'''
Created on May 12, 2013

@author: a;idfjasdflkj
'''
import sys
import socket
import re

def main(argv=sys.argv):
    NICK = "Twaltbot"
    IDENT = "Twaltbot"
    REALNAME = "Twaltbot"
    readbuffer = ""
    
    if len(sys.argv) == 3:
        HOST = gethost(sys.argv)
        PORT = getport(sys.argv)
    else:
        HOST = "irc.snoonet.org"
        PORT = 6667
            
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
            if "PING" in line:
                doPong(sock, line)
            if "$help" in line:
                doHelp(sock, line)
            elif "$mathify" in line:         
                doMathify(sock, line)


def doPong(sock, line):
    pong = "PONG %s\r\n" % line[1]
    sock.send(pong.encode())

def doHelp(sock, line):
    if line[1]=='PRIVMSG' and line[3] == ':$help':
        f = open("hello.txt", "r")
        lineslist = f.readlines();
        for words in lineslist:
            output = "PRIVMSG %s :%s\r\n" % (line[2], words)
            sock.send(output.encode())
            
def doMathify(sock, line):
    if line[1]=='PRIVMSG' and line[3] == ':$mathify':
        evalthis = line[4]
        if validMath(evalthis):
            evalthis = eval(evalthis)
            output = "PRIVMSG %s :%i\r\n" % (line[2], evalthis)
        else:
            output = "PRIVMSG %s :%s\r\n" % (line[2], "Invalid arguments for $mathify")
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
    valid = True
    numlist = re.split('[-/)(*+]+', arg)
    for val in numlist:
        if not val.isdigit():
             valid = False
    return valid
                    
main()
