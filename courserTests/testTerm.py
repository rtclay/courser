'''
Created on Aug 20, 2010

@author: richard
'''
from courser.CourserJsonDecoder import CourserJsonDecoder
from courser.CourserJsonEncoder import CourserJsonEncoder
from courser.Meetingset import Meetingset
from courser.Requirement import Requirement
from courser.Subject import Subject
from courser.Term import Term
import json
import unittest




class TermTest(unittest.TestCase):


    def setUp(self):
        self.terms= [Term("firstTerm", 2010, {}),
                     Term("secondTerm", 2010, {}),
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
        self.req0 = Requirement()
        
        for subj in self.subjects[:-3]:
            self.terms[0].addSubject(subj, Requirement(), Meetingset())


    def tearDown(self):
        del self.terms
        del self.subjects
        del self.req0

    def testHasSubject(self):
        for subj in self.subjects[:-3]:
            self.assertTrue(self.terms[0].hasSubject(subj), "Assert: %s is in %s" % (subj, self.terms[0]))
        for subj in self.subjects[-3:]:
            self.assertFalse(self.terms[0].hasSubject(subj), "Assert False: %s is in %s" % (subj, self.terms[0]))
            
    def testGetSubjectByName(self):
        self.assertEqual(self.subjects[0], self.terms[0].get_subject_by_name("18.01") )
        self.assertEqual(self.subjects[1], self.terms[0].get_subject_by_name("18.02") )

    def testAddSubject(self):
        #self.assertNotIn(self.subjects[0], self.terms[0], "Assert: %s is not in %s" % (self.subjects[0], self.terms[0]))
        self.terms[0].addSubject(self.subjects[0], self.req0, Meetingset())
        self.assertTrue(self.terms[0].hasSubject(self.subjects[0]), "After adding a subject, term must contain subject")
        
    def testRemoveSubject(self):
        self.terms[0].addSubject(self.subjects[0], self.req0, Meetingset())
        self.assertTrue(self.terms[0].hasSubject(self.subjects[0]), "After adding a subject, term must contain subject")
        self.terms[0].removeSubject(self.subjects[0])
        self.assertFalse(self.terms[0].hasSubject(self.subjects[0]), "After removing a subject, term must not contain subject")
    def testJSON(self):
        a = self.terms[0]
        string = json.dumps(a, cls = CourserJsonEncoder, indent = 2)
        b = json.loads(string, cls = CourserJsonDecoder)
        self.assertEqual(a, b)
    
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAddSubject']
    unittest.main()