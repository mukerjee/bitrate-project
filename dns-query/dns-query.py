#!/usr/bin/python
import socket

UDP_PORT = 53
UDP_IP = '128.2.184.224'

MESSAGE = "\x22\x16\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

data, addr = sock.recvfrom(1024)

print data
print addr
