'''
Created on Sep 04, 2010

@author: richard
'''
from courser.CourserJsonDecoder import CourserJsonDecoder
from courser.CourserJsonEncoder import CourserJsonEncoder
from courser.Meeting import Meeting
from courser.Meetingset import Meetingset
from courser.Subject import Subject
from random import random, randint, shuffle
import json
import unittest


class Test(unittest.TestCase):

    def makeMeetings(self, subj, minuteStart, minuteEnd):
        return Meetingset([Meeting(subj, minuteStart + x * 1440, minuteEnd + x * 1440) for x in range(5)])

    def setUp(self):
        self.subj = Subject("blank")
        self.meetings = [Meeting(self.subj, 1, 50),
                        Meeting(self.subj, 51, 100),
                        Meeting(self.subj, 101, 150),
                        Meeting(self.subj, 201, 250),
                        Meeting(self.subj, 251, 300),
                        ]
        self.meetingsRNoConf = sorted([Meeting(self.subj, x, x + y) for x, y in [(randint(301, 500), randint(0, 60) + 61) for z in range(5) ]])
        self.meetingsR = sorted([Meeting(self.subj, x, x + y) for x, y in [(randint(0, 240), randint(0, 60)) for z in range(5) ]])



        self.msets = [Meetingset([]),
                      Meetingset(self.meetings),
                      Meetingset(self.meetingsR),
                      Meetingset(self.meetingsRNoConf),
                      self.makeMeetings(self.subj, 485, 535),
                      self.makeMeetings(self.subj, 545, 595),
                      self.makeMeetings(self.subj, 560, 610)    #conflicts with previous set
                      ]


    def tearDown(self):
        pass
    def testCompare(self):
        self.assertEqual(Meetingset(), Meetingset(), "Assert Equal: %s == %s" % (Meetingset(), Meetingset()))
        self.assertNotEqual(Meetingset(), Meetingset([Meeting(self.subj)]), "Assert Equal: %s == %s" % (Meetingset(), Meetingset([Meeting(self.subj)])))
        self.assertEqual(self.msets[0], self.msets[0], "Assert Equal: %s == %s" % (self.msets[0], self.msets[0]))
        self.assertEqual(self.msets[1], self.msets[1], "Assert Equal: %s == %s" % (self.msets[1], self.msets[1]))


    def testAddMeeting(self):
        self.msets[0].addMeeting(self.meetings[0])
        self.assertIn(self.meetings[0], self.msets[0], "Assert: %s is in %s" % (self.meetings[0], self.msets[0]))


    def testRemoveMeeting(self):
        self.msets[1].removeMeeting(self.meetings[0])
        self.assertNotIn(self.meetings[1], self.msets[0], "Assert: %s is not in %s" % (self.meetings[1], self.msets[0]))

        self.msets[1].removeMeeting(self.meetings[1])
        self.assertNotIn(self.meetings[1], self.msets[1], "Assert: %s is not in %s" % (self.meetings[1], self.msets[1]))

    def testAddMeetingSet(self):
        self.msets[0].addMeetingSet(self.msets[1])
        for x in self.msets[1]:
            self.assertIn(x, self.msets[0], "Assert: %s is in %s" % (x, self.msets[0]))
    def testRemoveMeetingSet(self):
        pass
    def testIsBusyAtTime(self):
        time1 = 100
        self.assertFalse(self.msets[0].isBusyAtTime(time1), "Assert False: %s is busy at time %s" % (self.msets[0], time1))
        self.assertTrue(self.msets[1].isBusyAtTime(time1), "Assert: %s is busy at time %s" % (self.msets[1], time1))

    def testIsConflict(self):
        self.assertFalse(Meetingset().isConflict(Meetingset()), "Assert False: %s conflicts with %s" % (Meetingset(), Meetingset()))
        self.assertFalse(self.msets[0].isConflict(self.msets[1]), "Assert False: %s conflicts with %s" % (self.msets[0], self.msets[1]))
        self.assertFalse(self.msets[1].isConflict(self.msets[0]), "Assert False: %s conflicts with %s" % (self.msets[0], self.msets[1]))

        self.assertFalse(self.msets[1].isConflict(self.msets[3]), "Assert False: %s conflicts with %s" % (self.msets[1], self.msets[3]))
        self.assertFalse(self.msets[3].isConflict(self.msets[1]), "Assert False: %s conflicts with %s" % (self.msets[3], self.msets[1]))

        self.assertTrue(self.msets[1].isConflict(self.msets[1]), "Assert: %s conflicts with %s" % (self.msets[1], self.msets[1]))
        self.assertTrue(self.msets[1].isConflict(self.msets[2]), "Assert: %s conflicts with %s" % (self.msets[1], self.msets[2]))
        self.assertTrue(self.msets[2].isConflict(self.msets[1]), "Assert: %s conflicts with %s" % (self.msets[2], self.msets[1]))

    def testIsConflict2(self):
        self.assertFalse(self.msets[4].isConflict(self.msets[5]), "Assert False: %s conflicts with %s" % (self.msets[4], self.msets[5]))
        self.assertFalse(self.msets[5].isConflict(self.msets[4]), "Assert False: %s conflicts with %s" % (self.msets[5], self.msets[4]))

    def testIsConflict3(self):
        self.assertTrue(self.msets[5].isConflict(self.msets[6]), "Assert: %s conflicts with %s" % (self.msets[5], self.msets[6]))
        self.assertTrue(self.msets[6].isConflict(self.msets[5]), "Assert: %s conflicts with %s" % (self.msets[6], self.msets[5]))

    def testIsValid(self):
        ''' fails when shuffle returns the same order as the original
        '''
        self.assertTrue(self.msets[4].isValidMset(), "Assert: %s is Valid" % self.msets[4])
        shuffle(self.msets[4].meetings)

        self.assertFalse(self.msets[4].isValidMset(), "Assert False: %s is Valid" % self.msets[4])
        
    def testJSON(self):
        a = self.makeMeetings(self.subj, 560, 610)
        string = json.dumps(a, cls = CourserJsonEncoder)
        b = json.loads(string, cls = CourserJsonDecoder)
        print a
        print b
        print b.meetings
        print [Meeting(x) for x in b.meetings]
        self.assertEqual(a, b)







if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIsConflict']
    unittest.main()
