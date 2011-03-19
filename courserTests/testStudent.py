'''
Created on Aug 18, 2010

@author: richard
'''
from courser.ReqSingleSubject import ReqSingleSubject
from courser.Catalog import Catalog
from courser.ReqPartial import ReqPartial
from courser.Student import Student
from courserTests.Dataset import Dataset
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
        self.assertTrue(self.stud.subjectsTaken==[], "Assert True: %s == %s" % (self.stud.subjectsTaken, []))
    
#    def testSatisfiesReq(self):
#        self.stud.subjectsTaken = []
#        self.assertFalse(self.stud.satisfiesReq(self.dset.reqs63), "Assert False: self.stud.satisfiesReq(self.dset.reqs63)")
#        self.stud.subjectsTaken.extend(self.dset.reqs63.getSubjects())
#        print self.stud.subjectsTaken
#        print self.dset.reqs63
#        self.assertTrue(self.dset.reqs63.isSatisfied(list(self.dset.reqs63.getSubjects())), "Assert True: self.dset.reqs63 is satisfied with %s" % self.dset.reqs63.getSubjects())
#        self.assertTrue(self.stud.satisfiesReq(self.dset.reqs63), "Assert True: self.stud.satisfiesReq(self.dset.reqs63)")
    
    def testAvoid_Subject(self):
        self.stud.goals = ReqPartial([ReqSingleSubject(self.dset.get_subject_by_name("18.03")), ReqSingleSubject(self.dset.get_subject_by_name("18.06"))], 1)
        self.stud.subjectsTaken = [self.dset.get_subject_by_name("18.03"), self.dset.get_subject_by_name("18.06")]
        self.assertTrue(self.stud.satisfiesReq(self.stud.goals), "Assert True: self.stud.satisfiesReq(%s)" % self.stud.goals)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()