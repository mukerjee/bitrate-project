#!/usr/bin/python
import socket, sys
from common import genMessage, parseMessage
USAGE = 'Usage: %s [-r] <ip> <port> <servers> <LSAs> <logfile>' % (sys.argv[0])

ROUND_ROBIN = False

l = len(sys.argv)
if l < 6 or (sys.argv[1] == '-r' and l < 7):
    print USAGE
    exit(-1)

i = 1
if sys.argv[1] == '-r':
    ROUND_ROBIN = True
    i += 1

ip = sys.argv[i]
port = int(float(sys.argv[i+1]))
servers_file = sys.argv[i+2]
lsa_file = sys.argv[i+3]
log_file = sys.argv[i+4]

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip,port))
    data, addr = sock.recvfrom(1024)
    #print ":".join(c.encode('hex') for c in data)

    rr_addr = parseMessage(data, 1)

    (message, resolv) = genMessage(rr_addr[0], 0, ROUND_ROBIN, servers_file, lsa_file, addr, log_file)
    #print '%s --> %s' % (rr_addr[0], '.'.join([str(s) for s in resolv]))


    # print ":".join(c.encode('hex') for c in message)

    sock.sendto(message, addr)




