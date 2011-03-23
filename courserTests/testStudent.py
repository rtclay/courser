'''
Created on Aug 18, 2010

@author: richard
'''
from courser.Catalog import Catalog
from courser.CourserJsonDecoder import CourserJsonDecoder
from courser.CourserJsonEncoder import CourserJsonEncoder
from courser.ReqPartial import ReqPartial
from courser.ReqSingleSubject import ReqSingleSubject
from courser.Student import Student
from courserTests.Dataset import Dataset
import json
import unittest


class StudentTest(unittest.TestCase):


    def setUp(self):
        self.dset= Dataset()
        self.dset.dataSetup()
        self.catalog= Catalog(dict(zip([str(x) for x in self.dset.terms], self.dset.terms)))
        self.stud = Student()
        
        self.stud.goals = self.dset.reqs63


    def tearDown(self):
        pass
    
    def testInit(self):
        self.assertTrue(self.stud.subjects_taken==[], "Assert True: %s == %s" % (self.stud.subjects_taken, []))
    
#    def testSatisfiesReq(self):
#        self.stud.subjects_taken = []
#        self.assertFalse(self.stud.satisfiesReq(self.dset.reqs63), "Assert False: self.stud.satisfiesReq(self.dset.reqs63)")
#        self.stud.subjects_taken.extend(self.dset.reqs63.getSubjects())
#        print self.stud.subjects_taken
#        print self.dset.reqs63
#        self.assertTrue(self.dset.reqs63.isSatisfied(list(self.dset.reqs63.getSubjects())), "Assert True: self.dset.reqs63 is satisfied with %s" % self.dset.reqs63.getSubjects())
#        self.assertTrue(self.stud.satisfiesReq(self.dset.reqs63), "Assert True: self.stud.satisfiesReq(self.dset.reqs63)")
    
    def testAvoid_Subject(self):
        self.stud.goals = ReqPartial([ReqSingleSubject(self.dset.get_subject_by_name("18.03")), ReqSingleSubject(self.dset.get_subject_by_name("18.06"))], 1)
        self.stud.subjects_taken = [self.dset.get_subject_by_name("18.03"), self.dset.get_subject_by_name("18.06")]
        self.assertTrue(self.stud.satisfiesReq(self.stud.goals), "Assert True: self.stud.satisfiesReq(%s)" % self.stud.goals)
        
    def testJSON(self):
        a = self.stud
        string = json.dumps(a, cls = CourserJsonEncoder)
        b = json.loads(string, cls = CourserJsonDecoder)
        
        self.assertEqual(a, b)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()