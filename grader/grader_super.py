#!/usr/bin/python

import sys
sys.path.append('../common')

import os
import json
import unittest
from util import check_output, check_both

NETSIM = './netsim.py'

class Project3Test(unittest.TestCase):

    def __init__(self, test_name, topo=None):
        super(Project3Test, self).__init__(test_name)
        self.topo = topo

    ########### SETUP/TEARDOWN ##########

    # Run once per test suite
    @classmethod
    def setUpClass(cls):
        pass

    # Run once per test suite
    @classmethod
    def tearDownClass(cls):
        pass

    # Run once per test
    def setUp(self):
        self.start_netsim()

    # Run once per test
    def tearDown(self):
        check_output('killall -9 proxy')
        self.stop_netsim()


    ########## HELPER FUNCTIONS ##########

    def run_proxy(self, log, alpha, listenport, fakeip, dnsip, dnsport, serverip=''):
        run_bg('./proxy %s %s %s %s %s %s %s'\
            % (log, alpha, listenport, fakeip, dnsip, dnsport, serverip))

    def run_events(self, events_file=None, bg=False):
        cmd = '%s %s run' % (NETSIM, self.topo_dir)
        if events_file:
            cmd += ' -e %s' % events_file
        if bg:
            run_bg(cmd)
        else:
            check_output(cmd)

    def start_netsim(self):
        if topo_dir:
            check_output('%s %s start' % (NETSIM, self.topo_dir))
    
    def stop_netsim(self):
        if topo_dir:
            check_output('%s %s stop' % (NETSIM, self.topo_dir))

    # Returns log entries as lists, one at a time. Use in for loop,
    # e.g., "for entry in iter_log(file_path):".
    def iter_log(self, log_file):
        with open(log_file, 'r') as logf:
            for line in logf:
                line = line.strip()
                if line:
                    yield line.split(' ')
        logf.closed
    
    ########### TEST CASES ##########

    def test_proxy_simple(self):
        self.run_proxy('proxy.log', '1', '8081', '1.0.0.1', '0.0.0.0', '0', '2.0.0.1')
        self.run_events(os.path.join(self.topo_dir, 'simple.events'))  # TODO: make this file (David)

        # TODO: send a bunch of gets (until we think their estimate should have stabilized)

        # TODO: check what bitrate they're requesting
        for entry in iter_log('proxy.log'):
            pass # TODO: some kind of check here

        # TODO: check the hash of the last chunk we requested

    
    def test_proxy_adaptation(self):
        self.run_proxy('proxy.log', '1', '8081', '1.0.0.1', '0.0.0.0', '0', '2.0.0.1')
        self.run_events(os.path.join(self.topo_dir, 'adaptation-1600.events'))  # TODO: make this file (David)

        # TODO: send a bunch of gets
        # TODO: check their bitrate (log and/or hash?) -- should be 1000

        self.run_events(os.path.join(self.topo_dir, 'adaptation-800.events'))  # TODO: make this file (David)
        
        # TODO: send a bunch of gets
        # TODO: check their bitrate (log and/or hash?) -- should be 500

    
    def test_proxy_multiple_clients(self):
        self.run_proxy('proxy1.log', '1', '8081', '1.0.0.1', '0.0.0.0', '0', '3.0.0.1')
        self.run_proxy('proxy2.log', '1', '8082', '2.0.0.1', '0.0.0.0', '0', '4.0.0.1')
        self.run_events(os.path.join(self.topo_dir, 'multiple.events'))  # TODO: make this file (David)

        # TODO: send a bunch of gets to each (need threads so requests don't alternate??)
        # TODO: check BW each is getting; should be roughly equal (abs val of diff less than some thresh?)

    
    def test_proxy_alpha(self):
        pass

        # TODO: finish this test. I'm leaving it blank for now --- we can either
        # go with the script you put in the google doc, or do this, which might
        # be easier:

        # TODO: start one proxy with alpha 0.1
        # TODO: start link @ 1600 kbps
        # TODO: send a bunch of gets
        # TODO: set link to 800 kbps
        # TODO: send a bunch more gets
        # TODO: iterate through log file, counting how many requests it took for them to udpate their BW

        # TODO: repeat this for alpha = 0.5 and 0.9. Compare how long it took to switch bitrates for each to make sure alpha is functioning properly.



def emit_scores(test_results, test_values, test_categories):

    # Initialization
    test_scores = {}
    category_scores = {}
    for test, value in test_values.iteritems():
        test_scores[test] = test_values[test]  # start w/ max; deduct later
        category_scores[test_categories[test]] = 0  # init category scores to 0

    # Deduct points for failed tests
    for testcase in test_results.failures:
        test = testcase[0].id().split('.')[-1]
        test_scores[test] = 0

    # Sum category scores
    for test, score in test_scores.iteritems():
        category_scores[test_categories[test]] += score

    print test_scores  # for student's log
    print category_scores  # for student's log
    print json.dumps(category_scores)  # for autolab
