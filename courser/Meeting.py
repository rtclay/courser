'''
Created on Aug 17, 2010

@author: richard
'''


class Meeting(object):
    '''
    A meeting stores a start time, an end time, and a subject.  
    Time is considered to be an integer representing whole minutes past midnight on Sunday
    EG 00001 is 12:01 Monday morning
    EG 00480 is 8:00 Monday morning
    '''


    def __init__(self, startTime=0, endTime=1):
        '''
        Initialize startTime and endTime
        '''
        self.startTime = startTime
        self.endTime = endTime


    def __eq__(self, other):
        try:
            return self.startTime == other.startTime and self.endTime == other.endTime
        except:
            return False
    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        try:
            if self.startTime < other.startTime:
                return True
            if self.startTime == other.startTime:
                if self.endTime < other.endTime:
                    return True
            else:
                return False
        except:
            return False


    def __hash__(self):
        key = (self.startTime, self.endTime)
        return hash(key)

    def containsTime(self, time):
        '''Returns True IFF the time is after start time and before end time
        '''
        return time >= self.startTime and time <= self.endTime

    def isConflict(self, otherMeeting):
        """Tests if another meeting conflicts with this meeting.
        Returns True if there is a conflict, otherwise returns False.
        """
        if self.startTime == otherMeeting.startTime:
            return True

        if self.startTime < otherMeeting.startTime:
            earlierMeeting, laterMeeting = self, otherMeeting
        else:
            earlierMeeting, laterMeeting = otherMeeting, self

        if laterMeeting.startTime < earlierMeeting.endTime:
            return True

        return False


    def isValidMeeting(self):
        '''Returns True IFF end time is after start time, and start and end time fall within the week
        '''
        return (self.endTime > self.startTime) and (self.startTime >= 0) and self.endTime <= 10080

    def __repr__(self):
        return "<Meeting " + str(self.startTime) + " to " + str(self.endTime) + ">"

    def getDHM(self):
        '''Returns a tuple containing (STARTdays, STARThours, STARTminutes, ENDdays, ENDhours, ENDminutes)
        '''
        return (self.startTime / 1440, (self.startTime % 1440) / 60, (self.startTime % 60), self.endTime / 1440, (self.endTime % 1440) / 60, (self.endTime % 60))

    def __str__(self):
        return "<Meeting %d %d %d TO %d %d %d>" % self.getDHM()

    def to_json(self):
        return {"__class__": "Meeting",
            "startTime": self.startTime,
            "endTime": self.endTime,
            }

