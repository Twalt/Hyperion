'''
Created on May 12, 2013

@author: Arjun
'''
import sys
import socket

def main(argv=sys.argv):
    NICK = "Twaltbot"
    IDENT = "Twaltbot"
    REALNAME = "Twaltbot"
    readbuffer = ""
    connect = 0

    if len(argv) == 2:
        if isinstance(argv[0], int):
            if "." in argv[1]:
                HOST = argv[1]
                PORT = argv[0]
        elif isinstance(argv[1], int):
            if "." in argv[0]:
                HOST = argv[0]
                PORT = argv[1]
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
            if line[0] == "PING":
                pong = "PONG %s\r\n" % line[1]
                sock.send(pong.encode())
            if len(line) > 4:
                if line[1]=='PRIVMSG' and line[3] == ':Twaltbot' and line[4] == 'hello':
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
                    
main()
