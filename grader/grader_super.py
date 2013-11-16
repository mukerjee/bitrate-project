#!/usr/bin/python

import sys
sys.path.append('../common')

import os
import json
import unittest
import requests
import hashlib
from threading import Thread
from util import check_output, check_both, run_bg

NETSIM = '../netsim/netsim.py'
PROXY = '../proxy/proxy'

class Project3Test(unittest.TestCase):

    def __init__(self, test_name, topo_dir=None):
        super(Project3Test, self).__init__(test_name)
        self.topo_dir = topo_dir
        self.exc_info = []

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
        run_bg('%s %s %s %s %s %s %s %s'\
            % (PROXY, log, alpha, listenport, fakeip, dnsip, dnsport, serverip))

    def run_events(self, events_file=None, bg=False):
        cmd = '%s %s run' % (NETSIM, self.topo_dir)
        if events_file:
            cmd += ' -e %s' % events_file
        if bg:
            run_bg(cmd)
        else:
            check_output(cmd)

    def start_netsim(self):
        if self.topo_dir:
            check_output('%s %s start' % (NETSIM, self.topo_dir))
    
    def stop_netsim(self):
        if self.topo_dir:
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



    def check_gets(self, ip, port, num_gets, log_file, link_bw, expect_br, ignore=0, alpha=1.0):
        HASH_VALUE = {500: 'af29467f6793789954242d0430ce25e2fd2fc3a1aac5495ba7409ab853b1cdfa', 1000: 'f1ee215199d6c495388e2ac8470c83304e0fc642cb76fffd226bcd94089c7109'}

        # send a few gets (until we think their estimate should have stabilized)
        for i in xrange(num_gets):
            r = requests.get('http://%s:%s/vod/1000Seg2-Frag7' %(ip, port))

        # check what bitrate they're requesting
        tputs = []
        tput_avgs = []
        bitrates = []
        i = 0
        for entry in self.iter_log(log_file):
            i += 1
            if i <= ignore: continue
            tputs.append(float(entry[2]))
            tput_avgs.append(float(entry[3]))
            bitrates.append(int(float(entry[4])))
        tputs = tputs[1:-1]
        tput_avgs = tput_avgs[1:-1]
        bitrates = bitrates[1:-1]
        tput = float(sum(tputs))/len(tputs)
        tput_avg = float(sum(tput_avgs))/len(tput_avgs)
        bitrate = float(sum(bitrates))/len(bitrates)
        print tput, tput_avg, bitrate

        try: 
            self.assertTrue(abs(tput - link_bw) < .25*link_bw)
            self.assertTrue(abs(tput_avg - link_bw) < (1.0/float(alpha))*.25*link_bw)
            self.assertTrue(abs(bitrate - expect_br) < (1.0/float(alpha))*.1*expect_br)

            # check the hash of the last chunk we requested
            self.assertTrue(hashlib.sha256(r.content).hexdigest() == HASH_VALUE[expect_br])
        except Exception, e:
            self.exc_info = sys.exc_info()

    def check_errors(self):
        if self.exc_info:
            raise self.exc_info[1], None, self.exc_info[2]


    def get_log_switch_len(self, log, num_trials, start_br, end_br):
        entries = [e for e in self.iter_log(log)]
        entries = entries[num_trials:]
        switch = 0
        for i,e in enumerate(entries):
            if float(e[4]) == end_br and switch == 0:
                switch = i
            if float(e[4]) == start_br:
                switch = 0
        return switch

    def run_alpha_test(self, alpha, num_trials):
        self.run_proxy('proxy.log', alpha, '8081', '1.0.0.1', '0.0.0.0', '0', '2.0.0.1')
        self.run_events(os.path.join(self.topo_dir, 'adaptation-2000.events')) 
        self.check_gets('1.0.0.1', '8081', num_trials, 'proxy.log', 2000, 1000, 0, alpha)
        self.run_events(os.path.join(self.topo_dir, 'adaptation-900.events')) 
        self.check_gets('1.0.0.1', '8081', num_trials/2, 'proxy.log', 900, 500, num_trials, alpha)
        self.check_errors()
        return self.get_log_switch_len('proxy.log', num_trials, 1000, 500)



    ########### TEST CASES ##########

    def test_proxy_simple(self):
        self.run_proxy('proxy.log', '1', '8081', '1.0.0.1', '0.0.0.0', '0', '2.0.0.1')
        self.run_events(os.path.join(self.topo_dir, 'simple.events'))
        self.check_gets('1.0.0.1', '8081', 5, 'proxy.log', 900, 500)
        self.check_errors()
        print 'done test_proxy_simple'
    
    def test_proxy_adaptation(self):
        self.run_proxy('proxy.log', '1', '8081', '1.0.0.1', '0.0.0.0', '0', '2.0.0.1')
        self.run_events(os.path.join(self.topo_dir, 'adaptation-2000.events')) 
        self.check_gets('1.0.0.1', '8081', 5, 'proxy.log', 2000, 1000)
        self.run_events(os.path.join(self.topo_dir, 'adaptation-900.events')) 
        self.check_gets('1.0.0.1', '8081', 5, 'proxy.log', 900, 500, 5)
        self.check_errors()
        print 'done test_proxy_adaptation'
    
    def test_proxy_multiple_clients(self):
        self.run_proxy('proxy1.log', '1', '8081', '1.0.0.1', '0.0.0.0', '0', '3.0.0.1')
        self.run_proxy('proxy2.log', '1', '8082', '2.0.0.1', '0.0.0.0', '0', '3.0.0.1')
        self.run_events(os.path.join(self.topo_dir, 'multiple.events'))
        ts = []
        ts.append(Thread(target=self.check_gets, args= ('1.0.0.1', '8081', 10, 'proxy1.log', 950, 500)))
        ts.append(Thread(target=self.check_gets, args= ('2.0.0.1', '8082', 10, 'proxy2.log', 950, 500)))
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        self.check_errors()
        print 'done test_proxy_multiple_clients'
    
    def test_proxy_alpha(self):
        log_switch = []
        log_switch.append(self.run_alpha_test('0.1', 20))
        check_output('killall -9 proxy')
        log_switch.append(self.run_alpha_test('0.5', 10))
        check_output('killall -9 proxy')
        log_switch.append(self.run_alpha_test('0.9', 10))
        print log_switch
        self.assertTrue(log_switch[0] >= log_switch[1])
        self.assertTrue(log_switch[1] >= log_switch[2])
        print 'done test_proxy_alpha'


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
