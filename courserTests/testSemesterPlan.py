'''
Created on Sep 5, 2010

@author: richard
'''
from courser.Meeting import Meeting
from courser.Meetingset import Meetingset
from courser.Requirement import Requirement
from courser.SemesterPlan import SemesterPlan
from courser.Subject import Subject
from courser.Term import Term

import unittest



class Test(unittest.TestCase):

    def addSubjectToTerm(self, term, subj, req, minuteStart, minuteEnd):
        term.addSubject(subj, req, [self.makeMeetings(subj, minuteStart, minuteEnd)])

    def makeMeetings(self, subj, minuteStart, minuteEnd):
        return Meetingset([Meeting(subj, minuteStart+x*1440, minuteEnd+x*1440) for x in range(5)])

    def setUp(self):
        self.terms = [Term("FALL", 2010, {}),
                      Term("IAP", 2011, {}),
                      Term("SPRING", 2011, {}),
                      ]
        
        self.subjects = [Subject("18.01"),
                         Subject("18.02"),
                         Subject("18.03"),
                         Subject("18.04"),
                         Subject("6.01"),
                         Subject("6.02"),
                         Subject("6.003"),
                         Subject("6.004"),
                         Subject("6.005"),
                         Subject("11.01"),
                         Subject("IAP dance"),
                         Subject("IAP Baking"),
                         Subject("IAP Baking Advanced")

                         ]
        self.reqs = [Requirement([], 0, None, "Requires nothing"),
                     Requirement([], 1, self.subjects[0], "Requires 18.01"),
                     Requirement([], 1, self.subjects[1], "Requires 18.02"),
                     Requirement([], 1, self.subjects[2], "Requires 18.03"),
                     Requirement([], 1, self.subjects[4], "Requires 6.01"),
                     Requirement([Requirement([], 1, self.subjects[2], "Requires 18.03"), Requirement([], 1, self.subjects[4], "Requires 6.01")], 2, None, "Requires 18.03 and 6.01"),
                     
                     ]
        self.addSubjectToTerm(self.terms[0], self.subjects[0], self.reqs[0], 545, 595)
        self.addSubjectToTerm(self.terms[0], self.subjects[1], self.reqs[1], 545, 595)
        self.addSubjectToTerm(self.terms[0], self.subjects[4], self.reqs[4], 605, 655)
        self.addSubjectToTerm(self.terms[0], self.subjects[5], self.reqs[5], 605, 655)
        self.addSubjectToTerm(self.terms[0], self.subjects[2], self.reqs[2], 665, 725)
        self.addSubjectToTerm(self.terms[0], self.subjects[9], self.reqs[0], 735, 785)
        
        self.semesterPlans= [SemesterPlan(self.terms[0], [self.subjects[1], self.subjects[2]]),  #Solvable semester with no conflicts                             
                             SemesterPlan(self.terms[0], [self.subjects[0], self.subjects[1]]),  #Unsolvable semester with no solutions
                             SemesterPlan(self.terms[0], [])
                             ]
        
    


    def tearDown(self):
        del self.subjects
        del self.semesterPlans
        del self.terms


    def testGetUnits(self):
        pass
    
    def testRemoveCourse(self):
        self.assertTrue(self.semesterPlans[0].hasCourse(self.subjects[1]), "Assert: %s is in %s" % (self.subjects[1], self.semesterPlans[0]))
        self.semesterPlans[0].removeCourse(self.subjects[1])
        self.assertFalse(self.semesterPlans[0].hasCourse(self.subjects[1]), "Assert: %s is in %s" % (self.subjects[1], self.semesterPlans[0]))
    
    def testAddCourse(self):
        self.assertFalse(self.semesterPlans[0].hasCourse(self.subjects[0]), "Assert: %s is not in %s" % (self.subjects[0], self.semesterPlans[0]))
        self.semesterPlans[0].addCourse(self.subjects[0])
        self.assertTrue(self.semesterPlans[0].hasCourse(self.subjects[0]), "Assert: %s is in %s" % (self.subjects[0], self.semesterPlans[0]))
    
    def testHasCourse(self):
        self.assertFalse(self.semesterPlans[0].hasCourse(self.subjects[0]), "Assert: %s is not in %s" % (self.subjects[0], self.semesterPlans[0]))
        self.assertTrue(self.semesterPlans[0].hasCourse(self.subjects[1]), "Assert: %s is in %s" % (self.subjects[1], self.semesterPlans[0]))
    
    def testIsValid(self):
        pass
    
    
    def testScoreImportance(self):
        pass
    def testFindSwap(self):
        pass
    def testGetChildren(self):
        pass
    def testFillMeetings(self):
        pass
    def testCalcConflicts(self):
        pass
    def testSolve(self):
        #=======================================================================
        # print str(self.semesterPlans[0])
        # print str(self.semesterPlans[0].getSolution())
        # print str(self.semesterPlans[1].getSolution())
        # print str(self.semesterPlans[2].getSolution())
        #======================================================================= 
        self.assertTrue(self.semesterPlans[0].getSolution(), "Assert: %s is solvable" % self.semesterPlans[0])        
        self.assertFalse(self.semesterPlans[1].getSolution(), "Assert False: %s is solvable" % self.semesterPlans[1])
        self.assertTrue(self.semesterPlans[2].getSolution(), "Assert: %s is solvable" % self.semesterPlans[2])
        
    def testSolve2(self):
        self.assertTrue(self.semesterPlans[0].getSolution(), "Assert: %s is solvable" % self.semesterPlans[0])
        self.semesterPlans[0].addCourse(self.subjects[9])
        self.assertTrue(self.semesterPlans[0].getSolution(), "Assert: %s is solvable" % self.semesterPlans[0])
        self.semesterPlans[0].addCourse(self.subjects[0])
        self.assertFalse(self.semesterPlans[0].getSolution(), "Assert False: %s is solvable" % self.semesterPlans[0])
        
    def testSolve3(self):
        self.assertFalse(self.semesterPlans[1].getSolution(), "Assert False: %s is solvable" % self.semesterPlans[1])
        self.terms[0].addMeetingSet(self.subjects[1], self.makeMeetings(self.subjects[1], 10, 60))
        self.assertTrue(self.semesterPlans[1].getSolution(), "Assert: %s is solvable" % self.semesterPlans[1])
        self.terms[0].removeMeetingSet(self.subjects[1], self.makeMeetings(self.subjects[1], 10, 60))        
        self.assertFalse(self.semesterPlans[1].getSolution(), "Assert False: %s is solvable" % self.semesterPlans[1])  
    
    def testSolve4(self):
        self.assertFalse(self.semesterPlans[1].getSolution(), "Assert False: %s is solvable" % self.semesterPlans[1])
        self.terms[0].addMeetingSet(self.subjects[1], self.makeMeetings(self.subjects[1], 10, 60))
        self.assertTrue(self.semesterPlans[1].getSolution(), "Assert: %s is solvable" % self.semesterPlans[1])
        self.terms[0].removeMeetingSet(self.subjects[1], self.makeMeetings(self.subjects[1], 10, 60))
        self.assertFalse(self.semesterPlans[1].getSolution(), "Assert False: %s is solvable" % self.semesterPlans[1])        
        pass
     
#    def testCanAddMS(self):
#        FIX ME
#        self.assertFalse(self.terms[0].getMeetingSets(self.subjects[9])[0].isConflict(self.terms[0].getMeetingSets(self.subjects[1])[0]), "Assert: no conflict")
#        self.assertFalse(self.terms[0].getMeetingSets(self.subjects[9])[0].isConflict(self.terms[0].getMeetingSets(self.subjects[2])[0]), "Assert: no conflict")
#        
#        
#        self.assertTrue(self.semesterPlans[0].canAddMS(self.terms[0].getMeetingSets(self.subjects[9])[0]), "Assert: %s can add %s" % (self.semesterPlans[0], self.terms[0].getMeetingSets(self.subjects[9])[0]))


    
    def testReserveMS(self):
        pass
    def testProhibitMS(self):
        pass
    
    def testEQ(self):
        self.assertEqual(SemesterPlan(self.terms[0]), SemesterPlan(self.terms[0]))
        self.assertEqual(self.semesterPlans[0], self.semesterPlans[0])
        self.assertNotEqual(self.semesterPlans[0], self.semesterPlans[1])
    
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()