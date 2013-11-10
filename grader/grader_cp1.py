#!/usr/bin/python

import unittest
from grader_super import Project3Test, emit_scores

TEST_VALUES = {
    'test_one': 4,
    'test_two': 4,
    'test_three': 1,
    'test_four': 1
}

TEST_CATEGORIES = {
    'test_one': 'proxy',
    'test_two': 'proxy',
    'test_three': 'writeup',
    'test_four': 'proxy'
}

class Project3Checkpoint1Test(Project3Test):

    ########### SETUP/TEARDOWN ##########

    # Run once per test suite
    @classmethod
    def setUpClass(cls):
        super(Project3Checkpoint1Test, cls).setUpClass()

    # Run once per test suite
    @classmethod
    def tearDownClass(cls):
        super(Project3Checkpoint1Test, cls).tearDownClass()

    # Run once per test
    def setUp(self):
        super(Project3Checkpoint1Test, self).setUp()

    # Run once per test
    def tearDown(self):
        super(Project3Checkpoint1Test, self).tearDown()
    
    
    ########### TEST CASES ##########

    def test_four(self):
        print 'test four'
        self.assertEqual(1, 2)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Project3Checkpoint1Test('test_one'))
    suite.addTest(Project3Checkpoint1Test('test_two'))
    suite.addTest(Project3Checkpoint1Test('test_three'))
    suite.addTest(Project3Checkpoint1Test('test_four'))
    results = unittest.TextTestRunner(verbosity=2).run(suite)

    emit_scores(results, TEST_VALUES, TEST_CATEGORIES)
