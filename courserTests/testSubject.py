'''
Created on Sep 26, 2010

@author: richard
'''
from courser.Subject import Subject
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testEq(self):
        self.assertEqual(Subject("8.02"), Subject("8.02", 8), "Assert: %s must be %s" %(Subject("8.02"), Subject("8.02", 8)))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEq']
    unittest.main()