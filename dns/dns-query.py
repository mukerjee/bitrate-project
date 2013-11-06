#!/usr/bin/python
import socket, sys
from common import genMessage, parseMessage

UDP_IP = 'localhost'#'128.2.184.224'
UDP_PORT = 5353

query = sys.argv[1]
message = genMessage(query, 1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (UDP_IP, UDP_PORT))

data, addr = sock.recvfrom(1024)


# print ":".join(c.encode('hex') for c in M2)
# print ":".join(c.encode('hex') for c in data)


rr_addr = parseMessage(data, 0)
print rr_addr

