'''
Created on Sep 26, 2010

@author: richard
'''
from courser.CourserJsonDecoder import CourserJsonDecoder
from courser.CourserJsonEncoder import CourserJsonEncoder
from courser.Subject import Subject
from courserTests.Dataset import Dataset
import json
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        self.dset = Dataset()
        self.dset.dataSetup()


    def tearDown(self):
        pass


    def testEq(self):
        self.assertEqual(Subject("8.02"), Subject("8.02", 8), "Assert: %s must be %s" %(Subject("8.02"), Subject("8.02", 8)))
        self.assertEqual(Subject("18.02"), Subject("18.02"))
        self.assertNotEqual(Subject("8.02"), Subject("18.02"))
        
    def testJSON(self):
        a = Subject("8.02")
        string = json.dumps(a, cls = CourserJsonEncoder)
        b = json.loads(string, cls = CourserJsonDecoder)
        self.assertEqual(a.inCharge, b.inCharge)
        self.assertEqual(a, b)
        
    def testJSON2(self):
        a = self.dset.AUSubjects[0]
        string = json.dumps(a, cls = CourserJsonEncoder)
        b = json.loads(string, cls = CourserJsonDecoder)
        self.assertEqual(a.inCharge, b.inCharge)
        self.assertEqual(a, b)
        
    def testIn(self):
        subject_list = [Subject("A"), Subject("B"), Subject("C")]
        subject_set = set()
        subject_set.add(Subject("A"))
        subject_set.add(Subject("B"))
        subject_set.add(Subject("C"))
        
        self.assertIn(Subject("A"), subject_list)
        self.assertIn(Subject("A"), subject_set)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEq']
    unittest.main()