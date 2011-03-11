'''
Created on Aug 20, 2010

@author: richard
'''
from courser.Meeting import Meeting

class MeetingSetError(Exception):
    """Base class for exceptions in this module."""
    pass

class SortingError(MeetingSetError):
    """Exception raised if the meetingset's meetings are found to be out of order.

    Attributes:
        meetingList -- current state of the Mset's meetings
        msg  -- explanation of the error
    """

    def __init__(self, meetingList, msg="Unsorted meetings"):
        self.meetingList = meetingList
        self.msg = msg

class Meetingset(object):
    '''
    A meetingset contains meetings.
    '''


    def __init__(self, meetings=[]):
        self.meetings = sorted(meetings)
        if not self.isValid():
            raise SortingError(self.meetings)

    def __iter__(self):
        for n in self.meetings:
            if (isinstance(n, Meeting)):
                yield n

    def __eq__(self, other):
        try:
            return self.meetings == other.meetings
        except:
            return False
    def __hash__(self):
        key = frozenset(self.meetings)
        return hash(key)

    def __ne__(self, other):
        return not self.__eq__(other)

    def addMeeting(self, meeting):
        self.meetings.append(meeting)
        self.meetings.sort()
        if not self.isValid():
            raise SortingError(self.meetings)

    def removeMeeting(self, meeting):
        self.meetings.remove(meeting)
        self.meetings.sort()
        if not self.isValid():
            raise SortingError(self.meetings)

    def addMeetingSet(self, otherMS):
        self.meetings.extend(otherMS.meetings)
        self.meetings.sort()

        if not self.isValid():
            raise SortingError(self.meetings)

    def removeMeetingSet(self, otherMS):
        for meet in otherMS.meetings:
            self.meetings.remove(meet)
        self.meetings.sort()
        if not self.isValid():
            raise SortingError(self.meetings)

    def isBusyAtTime(self, time):
        #time is considered to be an integer representing whole minutes past midnight on Sunday
        #EG 00001 is 12:01 Monday morning
        #EG 00480 is 8:00 Monday morning
        for x in self.meetings:
            if x.containsTime(time):
                return True
            if x.startTime > time:
                break
        return False



    def isConflict(self, otherMeetingSet):
        """
        This function looks at the sorted lists A and B.  If the first class (call it CLASS) in either list
        begins after the first class in the other list ends, then the first class in the other list
        is guaranteed not to be a conflict and is removed.
        If there exist any classes left in the lists, and neither one ends before the other begins, then there is a conflict.
        """
        sortedMeetings = sorted(self.meetings)
        otherMeetings = sorted(otherMeetingSet.meetings)



        while sortedMeetings and otherMeetings:
            focus0 = sortedMeetings[0]
            focus1 = otherMeetings[0]


            if focus0.startTime > focus1.endTime:
                otherMeetings.pop(0)
                continue
            if focus1.startTime > focus0.endTime:
                sortedMeetings.pop(0)
                continue

            return True

        return False

    def isValid(self):
        return self.meetings == sorted(self.meetings)

    def __repr__(self):
        if self.meetings:
            return "<Meetingset " + str(self.meetings) + ">"
        else:
            return "<Meetingset EMPTY>"
    def to_json(self):
        return {"__class__": "MeetingSet",
                "meetings": self.meetings
                }

