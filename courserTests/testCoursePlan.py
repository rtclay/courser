'''
Created on Sep 16, 2010

@author: richard
'''
from courser.Catalog import Catalog
from courser.CoursePlan import CoursePlan
from courser.Requirement import Requirement
from courser.Subject import Subject
from courser.Term import Term
from courserTests.Dataset import Dataset
from math import factorial
import cPickle
import unittest



class Test(unittest.TestCase):


    def setUp(self):
        self.dset= Dataset()
        self.dset.dataSetup()
        self.catalog= Catalog(dict(zip([str(x) for x in self.dset.terms], self.dset.terms)))
        self.cplan = CoursePlan([], self.catalog)
        self.cplan.desired = self.cplan.solveReq(self.dset.reqs63, self.dset.terms[0]).getSubjects()
        
    def tearDown(self):
        pass


    def testBuildASP(self):
        term =self.dset.terms[0]
        is_avail = lambda subj: subj in term.getSubjects() and term.getReq(subj).isSatisfied(self.cplan.getSubjectsTakenBeforeTerm(term))
        eligible_subjects = filter(is_avail , set(self.cplan.getSubjectsRemaining(term)))
        
        print eligible_subjects
        
        binom = lambda n, k: factorial(n) / (factorial(k)*factorial(n-k))
        
        ASP = list(self.cplan.buildASP(term))
        sem_plan_count = [0]*(self.cplan.maxSubjectsPerTerm+1)
        for (x,y) in ASP:
            print x.getSubjects()
            sem_plan_count[len(x.getSubjects())] += 1 
        
        print sem_plan_count
        for x in range(1, self.cplan.maxSubjectsPerTerm+1):
            if x<= len(eligible_subjects):
                self.assertEqual(sem_plan_count[x], binom(len(eligible_subjects), x), "Assert Equal: number of semester plans length %s generated %s == %s" % (x, sem_plan_count[x], binom(len(eligible_subjects), x)))
    
        
        
    
    def testSolveReq(self):
        cplan = CoursePlan([], self.catalog)
        cplan.desired = cplan.solveReq(self.dset.reqs63, self.dset.terms[0])
        a =  cplan.solveReq(self.dset.reqs63, self.dset.terms[0]) 
        b =  cplan.solveReq(self.dset.reqs63, self.dset.terms[0])
        print sorted(a.getSubjects())
        print sorted(b.getSubjects())
        for x,y in cplan.subject_req_choices.items():
            print x, " : ", y
        self.assertTrue(a.getSubjects() == b.getSubjects(),  "Assert: %s equals %s" % (a.getSubjects(), b.getSubjects()))
    
    def testSolveReq2(self):
        cplan = CoursePlan([], self.catalog)
        cplan.desired = cplan.solveReq(self.dset.reqs63, self.dset.terms[0]).getSubjects()
        self.assertTrue(self.dset.reqs63.isSatisfied(cplan.getDesired()),  "Assert: %s satifies %s" % (cplan.getDesired(), self.dset.reqs63))
        
        
    def testgetSolChoice(self):

        self.assertEqual(self.cplan.solveReq(self.dset.terms[0].getReq(self.dset.subjects[0]), self.dset.terms[0]), Requirement(), "input: %s Expected %s: Actual: %s" % (self.dset.subjects[0], Requirement(), self.cplan.solveReq(self.dset.terms[0].getReq(self.dset.subjects[0]), self.dset.terms[0]) ))
        self.assertEqual(self.cplan.solveReq(self.dset.terms[0].getReq(self.dset.subjects[1]), self.dset.terms[0]), Requirement([],1, subj= self.dset.subjects[0]), "input: %s Expected %s: Actual: %s" % (self.dset.subjects[1], Requirement([],1, subj= self.dset.subjects[0]), self.cplan.solveReq(self.dset.terms[0].getReq(self.dset.subjects[1]), self.dset.terms[0]) ))
        
    
    def testPlotRemainingSemesters(self):
        self.cplan.desired = self.cplan.solveReq(self.dset.reqs63, self.dset.terms[0]).getSubjects()
        self.cplan.plotRemainingSemesters(self.dset.terms[0], 16) #Parameters: starting term, maximum number of semesters
        self.assertTrue(self.cplan.getSubjectsRemaining(self.cplan.getTermOfSatisfaction()) == set(), "Assert: no subjects remaining")
        
    def testDeepScore(self):
        #self.cplan.deepScoreSemesterPlan(sem_plan, 4, self.dset.terms[0])
        pass
    
    def testGetTermofSatisfaction(self):
        self.cplan.plotRemainingSemesters(self.dset.terms[0], 16)
        print self.cplan
        term = self.cplan.getTermOfSatisfaction()
        print term
        self.assertTrue(self.dset.reqs63.isSatisfied(self.cplan.getSubjectsTakenBeforeTerm(term)))
        
    def testEQ(self):
        self.assertEqual(CoursePlan(set(), self.catalog), CoursePlan(set(), self.catalog))
        self.assertEqual(self.cplan, self.cplan)
        self.assertNotEqual(CoursePlan(set(), self.catalog), self.cplan)

    def testPickle(self):
        
        string = cPickle.dumps(self.cplan)
        pick = cPickle.loads(string)
        
        print dir(self.cplan)== dir(pick)
        print len(self.cplan.desired), self.cplan.desired
        print len(pick.desired), pick.desired
        print sorted(self.cplan.desired ^ pick.desired)
        print set(sorted(self.cplan.desired ^ pick.desired))
        print self.cplan.desired.issubset(pick.desired), self.cplan.desired.issuperset(pick.desired)
        print self.cplan.term_info_dict.items() == pick.term_info_dict.items()
        print self.cplan == pick
#        for x, y in zip(dir(self.cplan), dir(pick)):
#            print x == y
#            if x!= y:
#                print x, y
        self.assertEqual(self.cplan, pick)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()