'''
Created on Nov 19, 2010

@author: richard
'''

from courser.CourserJsonDecoder import CourserJsonDecoder
from courser.CourserJsonEncoder import CourserJsonEncoder
from courser.ReqSingleSubject import ReqSingleSubject
from courserTests.Dataset import Dataset
import json
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        self.dset = Dataset()
        self.dset.dataSetup()



    def tearDown(self):
        del self.dset


    def testIsSatisfied(self):
        self.assertFalse(ReqSingleSubject(self.dset.subjects[0]).isSatisfied([]))
        self.assertTrue(ReqSingleSubject(self.dset.subjects[0]).isSatisfied([self.dset.subjects[0]]))
        
    def testJSON(self):
        a = ReqSingleSubject(self.dset.subjects[0])
        string_of_a = json.dumps(a, cls = CourserJsonEncoder)
        b = json.loads(string_of_a, cls = CourserJsonDecoder)
        print "a: ", a
        print "b: ", b
        self.assertEqual(a, b)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
