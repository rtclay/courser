 
from django.db import models
from courserwebview.models import Person, Student, Catalog, CoursePlan, Meeting, Meetingset, ReqNot, ReqPartial, ReqTotal, ReqSingleSubject, Requirement, SemesterPlan, Student, Term



# Create your models here.
#class CWVPerson(models.Model):
#    first_name = models.CharField(max_length=30)
#    last_name = models.CharField(max_length=30)
#    
#
#
#class CWVMeeting(models.Model):
#    start_time = models.PositiveIntegerField()
#    end_time = models.PositiveIntegerField()
#    subj = models.ForeignKey('CWVSubject')
#    
#    def __eq__(self, other):
#        try:
#            return self.start_time == other.start_time and self.end_time == other.end_time
#        except:
#            return False
#    def __ne__(self, other):
#        return not self == other
#
#    def __lt__(self, other):
#        try:
#            if self.start_time < other.start_time:
#                return True
#            if self.start_time == other.start_time:
#                if self.end_time < other.end_time:
#                    return True
#            else:
#                return False
#        except:
#            return False
#
#    def containsTime(self, time):
#        '''Returns True IFF the time is after start time and before end time
#        '''
#        #time is considered to be an integer representing whole minutes past midnight on Sunday
#        #EG 00001 is 12:01 Monday morning
#        #EG 00480 is 8:00 Monday morning
#        return time >= self.start_time and time <= self.end_time
#
#    def isConflict(self, otherMeeting):
#        """Tests if another meeting conflicts with this meeting.
#        Returns True if there is a conflict, otherwise returns False.
#        """
#        if self.start_time == otherMeeting.start_time:
#            return True
#
#        if self.start_time < otherMeeting.start_time:
#            earlierMeeting, laterMeeting = self, otherMeeting
#        else:
#            earlierMeeting, laterMeeting = otherMeeting, self
#
#        if laterMeeting.start_time < earlierMeeting.end_time:
#            return True
#
#        return False
#
#
#    def isValidMeeting(self):
#        '''Returns True IFF end time is after start time, and start and end time fall within the week
#        '''
#        return (self.end_time > self.start_time) and (self.start_time >= 0) and self.end_time <= 10080
#
#    def __unicode__(self):
#        return "<Meeting " + str(self.start_time) + " to " + str(self.end_time) + ">"
#
#class CWVMeetingSet(models.Model):
#    meetings = models.ManyToManyField("CWVMeeting")
#    
#    def __eq__(self, other):
#        try:
#            return self.meetings == other.meetings
#        except:
#            return False
#    def __hash__(self):
#        key = frozenset(self.meetings)
#        return hash(key)
#
#    def __ne__(self, other):
#        return not self.__eq__(other)
#    
#    def isConflict(self, otherMeetingSet):
#        """
#        This function looks at the sorted lists A and B.  If the first class (call it CLASS) in either list
#        begins after the first class in the other list ends, then the first class in the other list
#        is guaranteed not to be a conflict and is removed.
#        If there exist any classes left in the lists, and neither one ends before the other begins, then there is a conflict.
#        """
#        sortedMeetings = sorted(self.meetings)
#        otherMeetings = sorted(otherMeetingSet.meetings)
#
#
#
#        while sortedMeetings and otherMeetings:
#            focus0 = sortedMeetings[0]
#            focus1 = otherMeetings[0]
#
#            if focus0.startTime > focus1.endTime:
#                otherMeetings.pop(0)
#                continue
#            if focus1.startTime > focus0.endTime:
#                sortedMeetings.pop(0)
#                continue
#
#            return True
#
#        return False
#    
#    def __unicode__(self):
#        if self.meetings:
#            return "<Meetingset " + str(self.meetings) + ">"
#        else:
#            return "<Meetingset EMPTY>"
#
#class CWVSubject(models.Model):
#    name = models.CharField(max_length=64)
#    departmentCode = models.CharField(max_length=64)
#    course = models.CharField(max_length=64)
#    label = models.CharField(max_length=64)
#    inCharge = models.CharField(max_length=64)
#    subjectLevel = models.CharField(max_length=64)
#    totalUnits = models.PositiveIntegerField()
#    unitsLecture = models.PositiveIntegerField()
#    unitsLab = models.PositiveIntegerField()
#    unitsPreparation = models.PositiveIntegerField()
#    gradeType = models.CharField(max_length=16)
#    description = models.TextField()
#
#    def __lt__(self, other):
#        return self.name < other.name
#
#
#    def __eq__(self, other):        
#        try:
#            return self.name == other.name
#        except:
#            return False
#        
#    def __hash__(self):
#        return hash(self.name)
#    
#    def __unicode__(self):
#        return "<Subject: " + str(self.name) + ">"
#
#class CWVCatalog(models.Model):
#    terms = models.ManyToManyField("CWVTerm")
#    
#    def __eq__(self, other):
#        try:
#            return self.terms == other.terms
#        except:
#            return False
#
#    def __hash__(self):
#        return hash(self.terms)
#    
#    def getTerms(self):
#        return self.terms[:]
#
#
#    def getFollowingTerms(self, term):
#        '''Takes a term and returns a list containing all future terms in the catalog
#        '''
#        return filter(lambda x : x > term, sorted(self.getTerms()))
#
#    def getPreviousTerms(self, term):
#        '''Takes a term and returns a list containing all past terms in the catalog
#        '''
#        return filter(lambda x : x < term, sorted(self.getTerms()))
#
#
#class CWVSemesterPlan(models.Model):
#    courseplan = models.ForeignKey("CWVCoursePlan")
#class CWVCoursePlan(models.Model):
#    pass
#class CWVRequirement(models.Model):
#    numneeded = models.PositiveIntegerField()
#    singleSubject = models.ForeignKey("CWVSubject")
#    reqs = models.ManyToManyField("self")
#    name = models.CharField(max_length=64)
#class CWVReqNot(models.Model):
#    reqForNegation = models.ForeignKey("self")
#    name = models.CharField(max_length=64)
#class CWVReqPartial(models.Model):
#    numneeded = models.PositiveIntegerField()
#    reqs = models.ManyToManyField("self")
#    name = models.CharField(max_length=64)
#class CWVReqSingleSubject(models.Model):
#    singleSubject = models.ForeignKey("CWVSubject")    
#    name = models.CharField(max_length=64)
#class CWVReqTotal(models.Model):
#    numneeded = models.PositiveIntegerField()
#    reqs = models.ManyToManyField("self")
#    name = models.CharField(max_length=64)
#class CWVTerm(models.Model):
#
#    subjects = models.ManyToManyField("CWVSubject")
#    subject_data_set = models.ManyToManyField("CWVSubjectData")
    
class CWVSubjectData(models.Model):
    term = models.ForeignKey("CWVTerm")
    subject = models.ForeignKey("CWVSubject")
    requirement = models.ForeignKey("CWVRequirement")
    meetingsets = models.ManyToManyField("CWVMeetingset")