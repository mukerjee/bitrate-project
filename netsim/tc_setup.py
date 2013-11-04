#!/usr/bin/python

import sys
sys.path.append('../common')

import argparse
import hashlib
from util import check_output, check_both

TC='sudo /sbin/tc'


# Start traffic shaping on the specified interface by attaching a hierarchical
# token bucket to the interface (the "root" queue for that interface). We can
# then add individual classes to the "root" token bucket as needed.
def start():
    check_output('%s qdisc add dev %s root handle 1: htb default 0'\
        % (TC, args.interface))

    # make a default class for normal traffic
    check_output('%s class replace dev %s parent 1: classid 1:0 htb rate 100mbit ceil 100mbit'\
        % (TC, args.interface))



# Stop traffic shaping on the specified interface by removing the root queueing
# discipline on that interface (the token bucket we added in start())
def stop():
    out = check_both('%s qdisc del dev %s root' % (TC, args.interface), shouldPrint=False, check=False)
    if out[1] is not 0 and 'RTNETLINK answers: No such file or directory' not in out[0][0]:
        raise Exception("Error stopping traffic shaping")


# Update the traffic class associated with the pair of IP addresses specified
# as command line arguments
def update():
    if args.ip_pair == ['', '']:
        print 'You must specify a pair of IP addresses to update'
        return

    # hash the IP pair to a traffic class number ("sort" them first so we 
    # always hash them in the same order). Valid class numbers are 0 - 9999
    if args.ip_pair[0] < args.ip_pair[1]:
        ip_pair_str = args.ip_pair[0] + args.ip_pair[1]
    else:
        ip_pair_str = args.ip_pair[1] + args.ip_pair[0]
    traffic_class = int(hashlib.sha1(ip_pair_str).hexdigest(), 16) % 10000

    # Update the queues for the traffic class with the new BW/latency
    check_output('%s class replace dev %s parent 1: classid 1:%i htb rate %s ceil %s'\
        % (TC, args.interface, traffic_class, args.bandwidth, args.bandwidth))
    check_output('%s qdisc replace dev %s parent 1:%i handle %i: netem delay %s'\
        % (TC, args.interface, traffic_class, traffic_class, args.latency))

    # Update the rules mapping IP address pairs to the traffic class
    U32='%s filter replace dev %s protocol ip parent 1:0 prio 1 u32'\
        % (TC, args.interface)
    check_output('%s match ip dst %s match ip src %s flowid 1:%i'
        % (U32, args.ip_pair[0], args.ip_pair[1], traffic_class))
    check_output('%s match ip dst %s match ip src %s flowid 1:%i'
        % (U32, args.ip_pair[1], args.ip_pair[0], traffic_class))


def show():
    print '=============== Queue Disciplines ==============='
    check_output('%s -s qdisc show dev %s' % (TC, args.interface))
    print '\n=============== Traffic Classes ==============='
    check_output('%s -s class show dev %s' % (TC, args.interface))


def main():
    if args.command == 'start':
        start()
    elif args.command == 'stop':
        stop()
    elif args.command == 'update':
        update()
    elif args.command == 'show':
        show()


if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(description='Adjust traffic shaping settings')
    parser.add_argument('command', choices=['start','stop','show','update'], help='command: start or stop traffic shaping; show current filters; or update a filter')
    parser.add_argument('ip_pair', nargs='*', default=['', ''])
    parser.add_argument('-i', '--interface', default='lo', help='the interface to adjust')
    parser.add_argument('-b', '--bandwidth', default='100mbit', help='download bandwidth (e.g., 100mbit)')
    parser.add_argument('-l', '--latency', default='0ms', help='outbound latency (e.g., 20ms)')
    args = parser.parse_args()

    main()
