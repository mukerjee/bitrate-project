#!/usr/bin/python

import sys
sys.path.append('../common')

import json
import unittest

class Project3Test(unittest.TestCase):

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
        pass

    # Run once per test
    def tearDown(self):
        pass
    
    
    ########### TEST CASES ##########

    def test_one(self):
        print 'test one'
        self.assertEqual(1, 2)
    
    def test_two(self):
        print 'test two'
    
    def test_three(self):
        print 'test three'



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
