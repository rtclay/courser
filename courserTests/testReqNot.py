'''
Created on Nov 19, 2010

@author: richard
'''
from courser.ReqNot import ReqNot
from courser.Subject import Subject
from courserTests.Dataset import Dataset
import unittest
from courser.Requirement import Requirement


class Test(unittest.TestCase):


    def setUp(self):
        self.dset= Dataset()
        self.dset.dataSetup()



    def tearDown(self):
        del self.dset


    def testIsSatisfied(self):
        self.assertTrue(ReqNot([Requirement([], 1, self.dset.subjects[0])]).isSatisfied([]))
        self.assertFalse(ReqNot([Requirement([], 1, self.dset.subjects[0])]).isSatisfied([self.dset.subjects[0]]))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()