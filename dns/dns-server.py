#!/usr/bin/python
import socket, sys
from common import genMessage, parseMessage

UDP_PORT = 5353
BIND_IP = 'localhost'

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((BIND_IP,UDP_PORT))
    data, addr = sock.recvfrom(1024)
    rr_addr = parseMessage(data, 1)
    print rr_addr

    message = genMessage(rr_addr[0], 0)

    # print ":".join(c.encode('hex') for c in data)
    # print ":".join(c.encode('hex') for c in message)

    sock.sendto(message, addr)




