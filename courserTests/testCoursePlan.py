'''
Created on Sep 16, 2010

@author: richard
'''
from courser.Catalog import Catalog
from courser.CoursePlan import CoursePlan
from courser.Requirement import Requirement
from courser.Term import Term
from courserTests.Dataset import Dataset
import unittest



class Test(unittest.TestCase):


    def setUp(self):
        
        self.dset= Dataset()
        self.dset.dataSetup()
        self.catalog= Catalog(dict(zip([str(x) for x in self.dset.terms], self.dset.terms)))


    def tearDown(self):
        pass


    def testBuildASP(self):
        #print CoursePlan().buildASP(self.dset.terms[0], self.dset.AUSubjects)
        #self.assertEqual(1, 2, "Assert Equal: %s == %s" % (1, 2))
        pass
    
    def testSolveReq(self):
        cplan = CoursePlan(self.dset.reqs63.getSolution(self.dset.terms[0]).getSubjects(), self.catalog)
        a =  cplan.solveReq(self.dset.reqs63, self.dset.terms[0]) 
        b =  cplan.solveReq(self.dset.reqs63, self.dset.terms[0])
        print sorted(a.getSubjects())
        print sorted(b.getSubjects())
        for x,y in cplan.subject_req_choices.items():
            print x, " : ", y
        self.assertTrue(a.getSubjects() == b.getSubjects(),  "Assert: %s equals %s" % (a.getSubjects(), b.getSubjects()))
    
    def testSolveReq2(self):
        cplan = CoursePlan(self.dset.reqs63.getSolution(self.dset.terms[0]).getSubjects(), self.catalog)
        a =  cplan.solveReq(self.dset.reqs63, self.dset.terms[0]) 
        self.assertTrue(self.dset.reqs63.isSatisfied(a.getSubjects()),  "Assert: %s satifies %s" % (a.getSubjects(), self.dset.reqs63))
        
    def testSolveReq3(self):
        cplan = CoursePlan(self.dset.reqs63.getSolution(self.dset.terms[0]).getSubjects(), self.catalog)
        a =  cplan.solveReq(self.dset.reqs63, self.dset.terms[0]) 
        self.assertTrue(self.dset.reqs63.isValid(),  "Assert: %s is valid" % self.dset.reqs63)
        self.assertTrue(a.isValid(),  "Assert: %s is valid" % self.dset.reqs63)
        
    def testgetSolChoice(self):
        cplan = CoursePlan(None, self.catalog)

        self.assertEqual(cplan.getSolChoice(self.dset.terms[0].getReq(self.dset.subjects[0]), self.dset.terms[0]), Requirement(), "input: %s Expected %s: Actual: %s" % (self.dset.subjects[0], Requirement(), cplan.getSolChoice(self.dset.terms[0].getReq(self.dset.subjects[0]), self.dset.terms[0]) ))
        self.assertEqual(cplan.getSolChoice(self.dset.terms[0].getReq(self.dset.subjects[1]), self.dset.terms[0]), Requirement([],1, subj= self.dset.subjects[0]), "input: %s Expected %s: Actual: %s" % (self.dset.subjects[1], Requirement([],1, subj= self.dset.subjects[0]), cplan.getSolChoice(self.dset.terms[0].getReq(self.dset.subjects[1]), self.dset.terms[0]) ))
        
    
    def testPlotRemainingSemesters(self):
        cplan = CoursePlan(self.dset.reqs63.getSolution(self.dset.terms[0]).getSubjects(), self.catalog)
        cplan.plotRemainingSemesters(self.dset.terms[0], 16) #Parameters: starting term, maximum number of semesters
        self.assertTrue(cplan.getSubjectsRemaining(cplan.getTermOfSatisfaction()) ==[], "Assert: no subjects remaining")
        
    def testGetGoodSolution(self):
        cplan = CoursePlan(self.dset.reqs63.getSolution(self.dset.terms[0]).getSubjects(), self.catalog)
        cplan.plotRemainingSemesters(self.dset.terms[0], 16) #Parameters: starting term, maximum number of semesters
        self.assertTrue(cplan.getSubjectsRemaining(cplan.getTermOfSatisfaction()) ==[], "Assert: no subjects remaining")
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()