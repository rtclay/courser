'''
Created on Aug 23, 2010

@author: richard
'''
from courser.Meeting import Meeting
from courser.Subject import Subject
import cPickle
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        self.subj= Subject("blank")
        self.meeting0 = Meeting(self.subj, 900, 930)
        self.meeting1 = Meeting(self.subj, 900, 1000)
        self.meeting2 = Meeting(self.subj, 930, 1000)


    def tearDown(self):
        pass


    def testIsConflict(self):
        self.assertTrue(self.meeting0.isConflict(self.meeting1), "should be conflict")
        self.assertTrue(self.meeting1.isConflict(self.meeting0), "should be conflict")
        
    def testIsConflict2(self):
        self.assertFalse(self.meeting0.isConflict(self.meeting2), "should not be conflict")
        self.assertFalse(self.meeting2.isConflict(self.meeting0), "should not be conflict")
        
    def testCompare(self):
        self.assertTrue(self.meeting0 < self.meeting2, "Assert: %s < %s" % (self.meeting0, self.meeting2) )
        self.assertTrue(self.meeting0 < self.meeting1, "Assert: %s < %s" % (self.meeting0, self.meeting1) )
        self.assertTrue(self.meeting1 < self.meeting2, "Assert: %s < %s" % (self.meeting1, self.meeting2) )
        
    def testContainsTime(self):
        time1 = 900
        time2 = 901
        time3 = 929
        time4 = 930
        time5 = 931
        self.assertTrue(self.meeting0.containsTime(time1), "Assert: %s contains time %s" % (self.meeting0, time1))
        self.assertTrue(self.meeting0.containsTime(time2), "Assert: %s contains time %s" % (self.meeting0, time2))
        self.assertTrue(self.meeting0.containsTime(time3), "Assert: %s contains time %s" % (self.meeting0, time3))
        self.assertFalse(self.meeting0.containsTime(time5), "Assert untrue: %s contains time %s" % (self.meeting0, time5))
        self.assertFalse(self.meeting2.containsTime(time3), "Assert untrue: %s contains time %s" % (self.meeting0, time3))
        
    def testPickle(self):
        string = cPickle.dumps(self.meeting0)
        print string
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIsConflict']
    unittest.main()
    