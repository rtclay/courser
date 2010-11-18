'''
Created on Aug 17, 2010

@author: richard
'''


class Meeting(object):
    '''
    classdocs
    '''


    def __init__(self, subj, startTime=0, endTime=1 ):
        '''
        Constructor
        '''
        self.startTime = startTime
        self.endTime = endTime
        self.subj = subj
         
        
    def __cmp__(self, other):
        if isinstance(other, Meeting):
            if self.startTime < other.startTime:
                return -1
            if self.startTime == other.startTime:
                if self.endTime < other.endTime:
                    return -1
                if self.endTime == other.endTime:
                    return 0
                if self.endTime > other.endTime:
                    return 1
            if self.startTime > other.startTime:
                return 1
            
    def containsTime(self, time):
        #time is considered to be an integer representing whole minutes past midnight on Sunday
        #EG 00001 is 12:01 Monday morning
        #EG 00480 is 8:00 Monday morning
        return time >= self.startTime and time <= self.endTime  
        
    def isConflict(self, otherMeeting):
        """Tests if a meeting conflicts with this meeting.
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
    
    
    def isValid(self):
        return (self.endTime > self.startTime) and (self.startTime > 0) and self.endTime < 10080
    
    def __repr__(self):
        return "<Meeting "+ str(self.startTime) + " to " + str(self.endTime) +">"
    
    def getDHM(self):
        return (self.startTime /1440, (self.startTime%1440)/60, (self.startTime%60), self.endTime /1440, (self.endTime%1440)/60, (self.endTime%60))
    
    def __str__(self):
        return "<Meeting %d %d %d TO %d %d %d>" % self.getDHM()
    
    