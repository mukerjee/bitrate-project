#!/usr/bin/python
import socket, sys
from common import sendDNSQuery

UDP_IP = '5.0.0.1'
UDP_PORT = 5353
LOCAL_IP = '1.0.0.1'

print sendDNSQuery(sys.argv[1],LOCAL_IP,UDP_IP,UDP_PORT)

