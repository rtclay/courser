'''
Created on Nov 19, 2010

@author: richard
'''

from courser.ReqSingleSubject import ReqSingleSubject
from courserTests.Dataset import Dataset
import cPickle
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        self.dset= Dataset()
        self.dset.dataSetup()



    def tearDown(self):
        del self.dset


    def testIsSatisfied(self):
        self.assertFalse(ReqSingleSubject(self.dset.subjects[0]).isSatisfied([]))
        self.assertTrue(ReqSingleSubject(self.dset.subjects[0]).isSatisfied([self.dset.subjects[0]]))
        
    def testPickle(self):
        string = cPickle.dumps(ReqSingleSubject(self.dset.subjects[0]).isSatisfied([self.dset.subjects[0]]))
        print string


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()