'''
Created on May 12, 2013

@author: Arjun
'''
import sys
import socket
import re

HOST = ""
PORT = 0

def main(argv=sys.argv):
    global HOST
    global PORT
    
    NICK = "Twaltbot"
    IDENT = "Twaltbot"
    REALNAME = "Twaltbot"
    readbuffer = ""
    try:
        if len(sys.argv) >= 3:
            getAddress(sys.argv)
        else:
            HOST = "irc.snoonet.org"
            PORT = 6667
            
        sock = socket.socket();
        sock.connect((HOST, PORT))
        
        sock.send(("NICK %s\r\n" % NICK).encode())
        sock.send(("USER %s %s bla :%s\r\n" % 
                    (IDENT, HOST, REALNAME)).encode())
        if len(sys.argv) > 1:
            for param in sys.argv: 
                if param != "main.py" and not param.isdigit() and not "." in param:
                    doJoin(sock, str(param))
        else:
            doJoin(sock, "testlab8thing")
            
        
        events = dict()
        events['PING'] = doPong
        events[':$help'] = doHelp
        events[':$mathify'] = doMathify
        
        #makes sure connection always exists.
        #bot should not disconnect
        while 1:
            received = sock.recv(1024)
            readbuffer = readbuffer + received.decode("utf-8")
            temp=readbuffer.split("\n")
            readbuffer=temp.pop()
            
            for line in temp:
                print(line.decode("utf-8"))
                #logs connection info to terminal
                line=line.rstrip()
                line=line.split()
            #event loop
            for key in events:
                    if key in line:
                        doThis = events[key]
                        doThis(sock, line)
    except socket.gaierror:
		print("Invalid HOST / PORT values\n"
                "HOST and PORT must be first the two parameters.")
    except socket.error:
		print("Invalid HOST / PORT values\n"
                "HOST and PORT must be first the two parameters.")
    except KeyboardInterrupt:
        print("\nTerminating Bot")

#if the server sends a PING, it is trying to determine whether the 
#client has timed out. This function handles that request
def doPong(sock, line):
    if line[0] == 'PING':
        pong = "PONG %s\r\n" % line[1]
        sock.send(pong.encode())

#makes bot join the specified channel
def doJoin(sock, channel):
    sock.send(("JOIN #%s, \r\n" % (channel)).encode())
    
#reads data from file and prints out instructions for how to use
#$mathify
def doHelp(sock, line):
    if line[1]=='PRIVMSG' and line[3] == ':$help':
        f = open("hello.txt", "r")
        lineslist = f.readlines();
        for words in lineslist:
            output = "PRIVMSG %s :%s\r\n" % (line[2], words)
            sock.send(output.encode())

#executes parses the data from the message, calculates a result, and
#sends the result to be printed to the IRC
def doMathify(sock, line):
    if len(line) > 4:
        if line[1]=='PRIVMSG' and line[3] == ':$mathify':
            evalthis = line[4]
            if validMath(evalthis):
                evalthis = eval(evalthis)
                output = "PRIVMSG %s :%i\r\n" % (line[2], evalthis)
            else:
                output = "PRIVMSG %s :%s\r\n" % (line[2], 
                         "Invalid arguments for $mathify")
            sock.send(output.encode())

# sets the HOST and PORT global variables used to connect to the IRC
def getAddress(argv):
    global HOST
    global PORT
    if argv[1].isdigit():
        if "." in argv[2]:
            HOST = argv[2]
            PORT = int(argv[1])
    elif argv[2].isdigit():
        if "." in argv[1]:
            HOST = argv[1]
            PORT = int(argv[2])

# ensures the data being evaluated is valid, and does not contain
# any hidden secrets
def validMath(arg):
    valid = True
    numlist = re.split('[-/)(*+]+', arg)
    for val in numlist:
        if not val.isdigit():
             valid = False
    return valid
                    
main()
