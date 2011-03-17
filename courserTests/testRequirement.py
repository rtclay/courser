'''
Created on Aug 21, 2010

@author: richard
'''

from courser.CourserJsonDecoder import CourserJsonDecoder
from courser.CourserJsonEncoder import CourserJsonEncoder
from courser.Requirement import Requirement
from courser.Subject import Subject
from courserTests.Dataset import Dataset
import json
import unittest








class Test(unittest.TestCase):


    def setUp(self):
        self.dset= Dataset()
        self.dset.dataSetup()



    def tearDown(self):
        del self.dset

    
    def testConstruct(self):
        pass
        
    def testCompare(self):
        self.assertEqual(Requirement(), Requirement(), "Assert Equal: %s == %s" % (Requirement(), Requirement()))
        self.assertEqual(Requirement([], 1, self.dset.subjects[0], ""), Requirement([], 1, self.dset.subjects[0], ""), "Assert Equal: %s == %s" % (Requirement([], 1, self.dset.subjects[0], ""), Requirement([], 1, self.dset.subjects[0], "")))
        self.assertEqual(self.dset.reqs63, self.dset.reqs63, "Assert Equal: %s == %s" % (self.dset.reqs63, self.dset.reqs63))
        self.assertEqual(self.dset.reqs63.expand(self.dset.terms[0]), self.dset.reqs63.expand(self.dset.terms[0]), "Assert Equal: %s == %s" % (self.dset.reqs63.expand(self.dset.terms[0]), self.dset.reqs63.expand(self.dset.terms[0])))
        

    def testIsSatisfied(self):
        self.assertTrue(Requirement().isSatisfied([]))
        self.assertTrue(self.dset.physReq.isSatisfied([Subject("8.02")]))
        self.assertTrue(self.dset.physReq.isSatisfied([Subject("8.02"), Subject("18.01")]))
        self.assertTrue(self.dset.mathReq.isSatisfied([Subject("6.042"), Subject("18.03")]))
        self.assertTrue(self.dset.mathReq.isSatisfied([Subject("6.042"), Subject("18.06")]))
        self.assertTrue(self.dset.mathReq.isSatisfied([Subject("6.042"), Subject("18.06"), Subject("18.03")]))
        
        
        
        self.assertFalse(self.dset.physReq.isSatisfied([Subject("6.01")]))
        self.assertFalse(self.dset.mathReq.isSatisfied([Subject("18.03"), Subject("18.06")]))
    
    def testIsSatisfied2(self):
        print self.dset.reqs63.getSubjects()
        print self.dset.reqs63
        print self.dset.reqs63.isSatisfied(self.dset.reqs63.getSubjects())
        
        self.assertTrue(self.dset.reqs63.isSatisfied(self.dset.reqs63.getSubjects()))
        
        self.assertTrue(self.dset.physReq.isSatisfied(self.dset.physReq.getSubjects()))
        
    def testGetSubjects(self):
        self.assertEqual(self.dset.physReq.getSubjects(), set([self.dset.subjectDict["8.02"]]), "Assert Equal: %s == %s" % (self.dset.physReq.getSubjects(), [self.dset.subjectDict["8.02"]]))
        self.assertEqual(self.dset.introReq.getSubjects(), set([self.dset.subjectDict["6.01"], self.dset.subjectDict["6.02"]]), "Assert Equal: %s == %s" % (self.dset.introReq.getSubjects(), set([self.dset.subjectDict["6.01"], self.dset.subjectDict["6.02"]])))
        
        self.assertEqual(self.dset.AUSReq.getSubjects(), set(self.dset.AUSubjects), "Assert Equal: %s == %s" % (self.dset.AUSReq.getSubjects(), set(self.dset.AUSubjects)))

        
    def testIsTotal(self):
        self.assertTrue(self.dset.physReq.isTotal())
        self.assertTrue(self.dset.mathReq.isTotal())
        self.assertFalse(self.dset.AUSReq.isTotal())
        
    
    
    def testNumChoices(self):
        self.assertEqual(self.dset.physReq.getNumChoices(), 1)
        self.assertEqual(self.dset.mathReq.getNumChoices(), 2)
        self.assertEqual(Requirement().getNumChoices(), 0)
    
    def testAddSubject(self):
        self.reqNew=Requirement([], 0, None)
        self.assertTrue(self.reqNew.isSatisfied([]))
        self.reqNew.addSubject(Subject("8.01"))
        self.assertFalse(self.reqNew.isSatisfied([]))
        self.assertTrue(self.reqNew.isSatisfied([Subject("8.01")]))
        
    
    def testAddReq(self):
        self.reqNew=Requirement([], 0, None)
        self.reqNew.addReq(self.dset.mathReq)
        self.assertEqual(self.reqNew.getNumChoices(), 1, "must add a req to the list")
    
    def testExpand(self):
        a = self.dset.reqs63.expand(self.dset.terms[0]).squish()
        self.assertTrue(set(a.expand(self.dset.terms[0]).getSubjects()) == set(a.expand(self.dset.terms[0]).expand(self.dset.terms[0]).getSubjects()), "Assert: %s == %s" % (set(a.expand(self.dset.terms[0]).getSubjects()), set(a.expand(self.dset.terms[0]).expand(self.dset.terms[0]).getSubjects())))
        
    def testExpand2(self):
        for subj in self.dset.subjects[:20]: 
            print subj        
            req_to_check = self.dset.terms[0].getReq(subj)
            print "req_to_check is ", req_to_check
            #if the req is the same as the expansion of the req, then it had better be a class with no prerequisites 
            if req_to_check.expand(self.dset.terms[0]) == req_to_check: 
                print "expanded is same\n"
                self.assertTrue(len(req_to_check.reqs) ==0 and (req_to_check.singleSubject is None or self.dset.terms[0].getReq(req_to_check.singleSubject) ==Requirement()), "Assert empty req: %s reqs and  %s singlesubject" % (req_to_check.reqs, req_to_check.singleSubject))
    

        
            
    def testSquish(self):
        a = self.dset.reqs63.expand(self.dset.terms[0]).squish()
        
        self.assertTrue(a.getSubjects() == a.squish().getSubjects(), "Assert: %s == %s" % (a.getSubjects(), a.squish().getSubjects()))
        self.assertTrue(a.getSubjects() == a.squish().squish().getSubjects(), "Assert: %s == %s" % (a.getSubjects(), a.squish().squish().getSubjects()))
        self.assertTrue(Requirement().squish() == Requirement(), "Assert: %s == %s" % (Requirement().squish(), Requirement()))
    def testJSON(self):
        a = self.dset.physReq
        string = json.dumps(a, cls = CourserJsonEncoder, indent = 2)
        b = json.loads(string, cls = CourserJsonDecoder)
        self.assertEqual(a, b)
        
        
    
    
        

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetFlats']
    unittest.main()