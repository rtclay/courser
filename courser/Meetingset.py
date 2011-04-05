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
        self.msg = msg + str(meetingList)
    def __str__(self):
        return repr(self.msg)
        

class Meetingset(object):
    '''
    A meetingset contains meetings.  It can also test if a time conflicts with any of its meetings,
     or if another meetingset conflicts with any of its meetings.
    '''


    def __init__(self, meetings=[]):
        self.meetings = sorted(meetings)

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
        """ Add a meeting
        """
        self.meetings.append(meeting)
        self.meetings.sort()
        if not self.isValidMset():
            raise SortingError(self.meetings)

    def removeMeeting(self, meeting):
        """ Remove a meeting
        """
        self.meetings.remove(meeting)
        self.meetings.sort()
        if not self.isValidMset():
            raise SortingError(self.meetings)

    def addMeetingSet(self, otherMS):
        """ Add all the meetings in the other MeetingSet's meetings, then sort the meetings
        """
        self.meetings.extend(otherMS.meetings)
        self.meetings.sort()

        if not self.isValidMset():
            raise SortingError(self.meetings)

    def removeMeetingSet(self, otherMS):
        """ Add all the meetings in the other MeetingSet's meetings from this Meetingset's meetings, then sort this MeetingSet's meetings
        """
        for meet in otherMS.meetings:
            try:
                self.meetings.remove(meet)
            except ValueError:
                continue
        self.meetings.sort()
        if not self.isValidMset():
            raise SortingError(self.meetings)

    def isBusyAtTime(self, time):
        """Return True IFF time is included in any of this MeetingSet's Meetings
        """
        for x in self.meetings:
            if x.containsTime(time):
                return True
            if x.startTime > time:
                break
        return False



    def isConflict(self, otherMeetingSet):
        """
        Return True IFF any of the other MS's Meetings conflicts with any of this MeetingSet's Meetings.
        
        This function looks at the sorted lists A and B.  If the first Meeting in either list
        begins after the first Meeting in the other list ends, then the first Meeting in the other list
        is guaranteed not to be a conflict and is removed.
        If at the end there exist any Meetings left in the lists, and neither one ends before the other begins, then there is a conflict.
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

    def isValidMset(self):
        """Return True IFF the meetings are sorted, and each meeting is a valid meeting
        """
        if not self.meetings:
            return True
        else:
            return self.meetings == sorted(self.meetings) and reduce(lambda x, y: x and hasattr(y, "isValidMeeting") and y.isValidMeeting(), self.meetings, True)

    def __repr__(self):
        if self.meetings:
            return "<Meetingset " + str(self.meetings) + ">"
        else:
            return "<Meetingset EMPTY>"
    def to_json(self):
        return {"__class__": "MeetingSet",
                "meetings": self.meetings
                }

