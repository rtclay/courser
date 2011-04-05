 
import copy
from django.db import models




# Create your models here.
class CWVPerson(models.Model):
    '''
    A person model represents a person: instructor, student etc
    '''
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
class CWVStudent(CWVPerson):
    '''
    A student takes classes.  He has a goal that is a requirement, and a collection of subjects already taken.
    '''
    student_id = models.CharField(max_length=64)
    goal = models.ForeignKey("CWVRequirement") #a requirement that the student wants to meet.
    course_plan = models.ForeignKey("CWVCoursePlan")
    subjects_taken = models.ManyToManyField("CWVSubject")

    def __eq__(self, other):
        return self.student_id == other.student_id

    def __hash__(self):
        key = (self.student_id)
        return hash(key)

    def addSubject_taken(self, subject_or_subjects):
        try:
            it = iter(subject_or_subjects)
            self.subjects_taken.extend(subject_or_subjects)
        except TypeError:
            self.subjects_taken.append(subject_or_subjects)

    def getProgress(self, req):
        return req.getProgress(self.subjects_taken)

    def satisfiesReq(self, req):
        return req.isSatisfied(self.subjects_taken)

    def avoid_Subject(self, subject):
        self.goals = CWVReqTotal([self.goals, CWVReqNot(CWVReqSingleSubject(subject))])

class CWVMeeting(models.Model):
    '''
    A meeting stores a start time, an end time, and a subject.  Time is considered to be an integer representing whole minutes past midnight on Sunday
        #EG 00001 is 12:01 Monday morning
        #EG 00480 is 8:00 Monday morning
    '''
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()
    subj = models.ForeignKey('CWVSubject')
    
    def __eq__(self, other):
        try:
            return self.start_time == other.start_time and self.end_time == other.end_time
        except:
            return False
    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        try:
            if self.start_time < other.start_time:
                return True
            if self.start_time == other.start_time:
                if self.end_time < other.end_time:
                    return True
            else:
                return False
        except:
            return False

    def containsTime(self, time):
        '''Returns True IFF the time is after start time and before end time
        '''
        #time is considered to be an integer representing whole minutes past midnight on Sunday
        #EG 00001 is 12:01 Monday morning
        #EG 00480 is 8:00 Monday morning
        return time >= self.start_time and time <= self.end_time

    def isConflict(self, otherMeeting):
        """Tests if another meeting conflicts with this meeting.
        Returns True if there is a conflict, otherwise returns False.
        """
        if self.start_time == otherMeeting.start_time:
            return True

        if self.start_time < otherMeeting.start_time:
            earlierMeeting, laterMeeting = self, otherMeeting
        else:
            earlierMeeting, laterMeeting = otherMeeting, self

        if laterMeeting.start_time < earlierMeeting.end_time:
            return True

        return False


    def isValidMeeting(self):
        '''Returns True IFF end time is after start time, and start and end time fall within the week
        '''
        return (self.end_time > self.start_time) and (self.start_time >= 0) and self.end_time <= 10080

    def __unicode__(self):
        return "<Meeting " + str(self.start_time) + " to " + str(self.end_time) + ">"

class CWVMeetingSet(models.Model):
    '''
    A meetingset contains meetings. 
    '''
    meetings = models.ManyToManyField("CWVMeeting")
    
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
    
    def isBusyAtTime(self, time):
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
    
    def __unicode__(self):
        if self.meetings:
            return "<Meetingset " + str(self.meetings) + ">"
        else:
            return "<Meetingset EMPTY>"

class CWVSubject(models.Model):
    name = models.CharField(max_length=64)
    departmentCode = models.CharField(max_length=64)
    course = models.CharField(max_length=64)
    label = models.CharField(max_length=64)
    inCharge = models.CharField(max_length=64)
    subjectLevel = models.CharField(max_length=64)
    totalUnits = models.PositiveIntegerField()
    unitsLecture = models.PositiveIntegerField()
    unitsLab = models.PositiveIntegerField()
    unitsPreparation = models.PositiveIntegerField()
    gradeType = models.CharField(max_length=16)
    description = models.TextField()

    def __lt__(self, other):
        return self.name < other.name


    def __eq__(self, other):        
        try:
            return self.name == other.name
        except:
            return False
        
    def __hash__(self):
        return hash(self.name)
    
    def __unicode__(self):
        return "<Subject: " + str(self.name) + ">"

class CWVCatalog(models.Model):
    terms = models.ManyToManyField("CWVTerm")
    
    def __eq__(self, other):
        try:
            return self.terms == other.terms
        except:
            return False

    def __hash__(self):
        return hash(self.terms)
    
    def getTerms(self):
        return self.terms[:]


    def getFollowingTerms(self, term):
        '''Takes a term and returns a list containing all future terms in the catalog
        '''
        return filter(lambda x : x > term, sorted(self.getTerms()))

    def getPreviousTerms(self, term):
        '''Takes a term and returns a list containing all past terms in the catalog
        '''
        return filter(lambda x : x < term, sorted(self.getTerms()))
    
    def getNextTerm(self, term):
        return self.getFollowingTerms(term)[0]


class CWVSemesterPlan(models.Model):
    '''
    A semester plan is a collection of subjects and the ability to test if 
    any selection of the subjects' meetingsets will allow all classes to be taken in the term.
    '''
    courseplan = models.ForeignKey("CWVCoursePlan")
    desired = models.ManyToManyField("CWVSubject")
    reserved_times = models.ForeignKey("CWVMeetingSet")
    term = models.ForeignKey("CWVTerm")
    
    
    def __eq__(self, other):
        try:
            return self.desired == other.desired and self.term == other.term and self.reserved_times == other.reserved_times
        except:
            return False

    def __hash__(self):
        key = (frozenset(self.desired), self.term, self.reserved_times)
        return hash(key)

    def __ne__(self, other):
        return not self.__eq__(other)

    def getSubjects(self):
        return self.desired.copy()

    def getUnits(self):
        return reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]), [subj.getUnits() for subj in self.desired])

    def getTerm(self):
        return self.term

    def removeSubject(self, course):
        if course in self.getSubjects():
            self.desired.remove(course)

    def addSubject(self, course):
        self.desired.add(course)

    def hasSubject(self, course):
        return course in self.getSubjects()


    def isValid(self):
        for subj in self.desired:
            if not self.term.hasSubject(subj):
                return False
        return True


    def findSwap(self, subjToSwapOut, desiredSubjects):
        pass
    
    def canAddMS(self, mset):
        return not self.reserved_times.isConflict(mset)

    def getSolution(self):
        '''Returns a SemesterPlan that has all the desired classes assigned to meetingsets
        '''
        duplicate = CWVSemesterPlan(self.term, self.desired.copy(), CWVMeetingSet(sorted(self.reserved_times.meetings)))
        #First, deal with immediate disqualifications
        #if there is a subject with no selectable meeting times, return a failure
        if [] in [duplicate.term.getMeetingSets(x) for x in duplicate.desired]:
            return None
        #if there are somehow no desired classes, return self
        if not len(duplicate.desired):
            return duplicate

        #Second, deal with more complex cases
        #subj, subjMSList = duplicate.desired.popitem()
        for (subj, subjMSList) in zip(duplicate.desired, map(lambda x : duplicate.term.getMeetingSets(x), duplicate.desired)):

            duplicate.desired.remove(subj)

            #the subject under consideration has now been removed from the list of desired classes
            for mset in subjMSList:
                if duplicate.canAddMS(mset):
                    duplicate.reserved_times.addMeetingSet(mset)
                    solution = duplicate.getSolution()
                    if solution:
                        return solution
                    else:
                        duplicate.reserved_times.removeMeetingSet(mset)
                        continue

            duplicate.desired.add(subj)


        return None
    
    
class CWVCoursePlan(models.Model):
    catalog = models.ForeignKey("Catalog")
    
class CWVRequirement(models.Model):
    num_needed = models.PositiveIntegerField()
    singleSubject = models.ForeignKey("CWVSubject")
    reqs = models.ManyToManyField("self")
    name = models.CharField(max_length=64)
    
    def __eq__(self, other):
        try:
            return self.reqs == other.reqs and self.singleSubject == other.singleSubject and self.num_needed == other.num_needed
        except:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        key = (frozenset(self.reqs), self.singleSubject, self.num_needed)
        return hash(key)

    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns True or False according to whether the req is satisfied
        '''
        if self.isLeaf():
            if self.singleSubject is None:
                return True
            else:
                return self.singleSubject in classesTaken
        else:
            return reduce(lambda x, y: x + y.isSatisfied(classesTaken), self.reqs, 0) >= self.num_needed

    def getnum_needed(self):
        return self.num_needed

    def getReqs(self):
        '''Returns a set containing the requirement's subrequirements
        Returns an empty set if there are no subrequirements
        '''
        if self.reqs:
            return self.reqs
        else:
            return set()

    def setReqs(self, set_of_Reqs):
        self.reqs = set_of_Reqs

    def getNumChoices(self):
        if self.isLeaf():
            if self.singleSubject is None:
                return 0
            else:
                return 1 #the single subject presents one choice
        else:
            return len(self.reqs)

    def addSubject(self, subject):
        #if the subject isnt already in the top layer of requirements, add a new leaf req to self's list containing the subj
        if not(subject in [x.getSingleSubj for x in self.reqs]):
            self.num_needed += 1
            self.reqs.append(CWVRequirement(subj=subject))

    def addReq(self, req):
        #if the subject isnt already in the top layer of requirements, add the req to self's reqs
        if not(req in self.reqs):
            self.num_needed = self.num_needed + 1
            self.reqs.append(req)

    def removeReq(self, req):
        if req in self.reqs:
            self.reqs.remove(req)
            self.num_needed = self.num_needed - 1

    def generateReq(self, listOfSubjects, num_needed):
        listOfReqs = []

        for subj in listOfSubjects:
            listOfReqs.append(CWVRequirement([], 0, subj))
        return CWVRequirement(listOfReqs, num_needed, subj)


    def squish(self):
        '''Returns a new requirement that has empty shells stripped away        
        '''
        if not self.reqs:
            return self


        if len(self.reqs) == 1 and self.num_needed == 1:
            return self.reqs[0].squish()

        newReq = CWVRequirement(self.reqs[:], self.num_needed, self.singleSubject)
        #Note: because it iterates on self.reqs and removes from a copy, there is no longer the problem of deleting from an iterating sequence 
        for subreq in self.reqs:
            if hasattr(subreq, "reqs") and bool(subreq.reqs) & (subreq.num_needed == len(subreq.reqs)):
                for subsubreq in subreq:
                    newReq.addReq(subsubreq.squish())
                newReq.removeReq(subreq)
        return newReq

    def completeSquish(self):
        temp = copy.copy(self)
        #temp = Requirement(self.reqs[:], self.num_needed, self.singleSubject)
        while temp != temp.squish():
            temp = temp.squish()
        return temp


    def expand(self, term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''
        if self.isBlank():
            return self
        #if it doesn't have sub requirements, just look at the single subject
        if not self.reqs:
            #if it is an empty requirement, return self
            if self.singleSubject is None:
                return self
            #if the req has a single subject, expand that subject
            subject_req = term.getReq(self.singleSubject)

            if subject_req.isBlank():
                #if self's single subject has a blank requirement, return self
                return self
            else:
                return CWVRequirement([self, subject_req.expand(term)], 2)


        #in this case, the req has multiple subreqs
        return CWVRequirement([req.expand(term) for req in self.reqs], self.num_needed)



    def getSubjects(self):
        '''Returns a set of all the subjects touched by a requirement
        '''
        subjects = set()
        if self.isLeaf():
            subjects.add(self.singleSubject)
        else:
            for req in self.reqs:
                subjects |= req.getSubjects()

        return subjects

    def getSingleSubj(self):
        return self.singleSubject

    def getProgress(self, classesTaken):
        if self.isLeaf():
            if self.singleSubject in classesTaken:
                return 1
            else:
                return 0
        else:
            #return the progress of its constituent requirements
            return reduce(lambda x, y: x + y.getProgress(classesTaken), self.reqs, 0)

    def isValidReq(self):
        try:
            return reduce(lambda x, y: x and y.isValidReq(), self.reqs, True) and self.getNumChoices() >= 0 and self.num_needed <= self.getNumChoices()

        except:
            return False


    def getComplexity(self, term):
        '''Returns a positive number representing the complexity of the req's subordinate requirements
        Roughly, complexity increases with the depth and number of the req's sub-requirements
        Every subreq will be less complex than its parent
        When the Requirement class becomes an interface, this function will return a notImplementedError for the Requirement Class; subclasses will define.
        '''

        return 1.5 * reduce(lambda x, y: x + y.getComplexity(term), self.reqs, 0) + int(self.isLeaf())

    def isLeaf(self):
        '''Tests whether self has any subordinate requirements
        '''
        return not self.reqs

    def isTotal(self):
        '''Tests whether the top level of this requirement requires all of its components to be satisfied
        Returns True IFF self is a leaf or self.num_needed == self.getNumChoices()
        '''
        if self.isLeaf():
            return True
        else:
            return (self.num_needed == self.getNumChoices())
    def isPartial(self):
        '''Tests whether the top level of this requirement requires only part of its components to be satisfied
        Returns True IFF self.num_needed != self.getNumChoices()
        '''
        return (self.num_needed != self.getNumChoices())

    def isBlank(self):
        return (self.num_needed == 0) & (self.singleSubject == None)
class CWVReqNot(CWVRequirement):
    reqForNegation = models.ForeignKey("self")
    name = models.CharField(max_length=64)
    def __eq__(self, other):
        try:
            return self.reqForNegation == other.reqForNegation
        except:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        key = (self.reqForNegation)
        return hash(key)

    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns the opposite truth value to whether self is satisfied by the classesTaken
        '''
        return not self.reqForNegation.isSatisfied(classesTaken)

    def expand(self, term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''

        #the req has multiple subreqs
        return CWVReqNot(self.reqForNegation.expand(term))

    def getProgress(self, classesTaken):
        if self.isSatisfied(classesTaken):
            return 1
        else:
            return 0
    def getNumChoices(self):
        return 1

    def getSubjects(self):
        return None

    def getComplexity(self, term):
        return self.reqForNegation.getComplexity(term)

    def isLeaf(self):
        '''Tests whether self has any subordinate requirements
        '''
        return False
class CWVReqPartial(CWVRequirement):
    num_needed = models.PositiveIntegerField()
    reqs = models.ManyToManyField("self")
    name = models.CharField(max_length=64)
    def __eq__(self, other):
        try:
            return self.getReqs() == other.getReqs() and self.num_needed == other.num_needed
        except:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        key = (self.reqs, self.num_needed)
        return hash(key)

    def getSubjects(self):
        subjects = set()
        for req in self.reqs:
            subjects |= req.getSubjects()

        return subjects

    def getNumChoices(self):
        return len(self.reqs)

    def getProgress(self, classesTaken):
        #return the progress of its constituent requirements
        return reduce(lambda x, y: x + y.getProgress(classesTaken), self.reqs, 0)

    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns whether enough component requirements have been satisfied
        '''
        return reduce(lambda x, y: x + y.isSatisfied(classesTaken), self.reqs, 0) >= self.num_needed

    def expand(self, term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''
        #the req has multiple subreqs
        return CWVReqPartial([req.expand(term) for req in self.reqs], self.num_needed)

    def getComplexity(self, term):
        return 1.5 * reduce(lambda x, y: x + y.getComplexity(term), self.reqs, 0)

    def isLeaf(self):
        '''Tests whether self has any subordinate requirements
        '''
        return False
class CWVReqSingleSubject(CWVRequirement):
    singleSubject = models.ForeignKey("CWVSubject")    
    name = models.CharField(max_length=64)
    
    def __eq__(self, other):
        try:
            return self.singleSubject == other.singleSubject
        except:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        key = (self.singleSubject)
        return hash(key)

    def isSatisfied(self, classesTaken):
        '''Returns T/F if self.singlesubject is in classesTaken
        '''
        return self.singleSubject in classesTaken

    def getSubjects(self):
        subjs = set()
        subjs.add(self.singleSubject)
        return subjs

    def expand(self, term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''
        #if it is an empty requirement, return self
        if self.singleSubject is None:
            return self
        else:
            #if the req has a single subject, expand that subject
            subject_req = term.getReq(self.singleSubject)

            if subject_req.isBlank():
                #if self's single subject has a blank requirement, return self
                return self
            else:
                return CWVReqTotal([self, subject_req.expand(term)])

    def getProgress(self, classesTaken):
        if self.singleSubject in classesTaken:
            return 1
        else:
            return 0

    def getComplexity(self, term):
        '''If the single subject has a blank requirement, returns 1.  Otherwise returns 1+ the complexity of that subject's requirement
        '''
        subj_req = term.getReq(self.singleSubject)
        if subj_req.isBlank():
            return 1
        else:
            return 1 + self.expand(term).getComplexity()

    def isLeaf(self):
        '''Tests whether self has any subordinate requirements
        '''
        return True

    def isValidReq(self):
        if self.singleSubject and hasattr(self.singleSubject, "isValidSubject") and self.singleSubject.isValidSubject():
            return True
        else:
            return False

    def squish(self):
        return self
class CWVReqTotal(CWVReqPartial):
    num_needed = models.PositiveIntegerField()
    reqs = models.ManyToManyField("self")
    name = models.CharField(max_length=64)
    
    def __eq__(self, other):
        try:
            return self.reqs == other.reqs
        except:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        key = (self.reqs)
        return hash(key)

    def getSubjects(self):
        subjects = set()
        for req in self.reqs:
            subjects |= req.getSubjects()

        return set(subjects)

    def getProgress(self, classesTaken):
        #return the progress of its constituent requirements
        return reduce(lambda x, y: x + y.getProgress(classesTaken), self.reqs, 0)

    def getNumChoices(self):
        return len(self.reqs)

    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns whether enough component requirements have been satisfied
        '''
        return reduce(lambda x, y: x + y.isSatisfied(classesTaken), self.reqs, 0) >= self.num_needed

    def expand(self, term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''
        #the req has multiple subreqs
        return CWVReqTotal([req.expand(term) for req in self.reqs])

    def squish(self):
        '''Returns a new requirement that has empty shells stripped away        
        '''
        if not self.reqs:
            return self


        if len(self.reqs) == 1 and self.num_needed == 1:
            return self.reqs[0].squish()

        newReq = CWVReqTotal(self.reqs[:])
        #Note: because it iterates on self.reqs and removes from a copy, there is no longer the problem of deleting from an iterating sequence 
        for subreq in self.reqs:
            if hasattr(subreq, "reqs") and bool(subreq.reqs) & (subreq.num_needed == len(subreq.reqs)):
                for subsubreq in subreq:
                    newReq.addReq(subsubreq.squish())
                newReq.removeReq(subreq)
        return newReq
    def getComplexity(self, term):
        return 1.5 * reduce(lambda x, y: x + y.getComplexity(term), self.reqs, 0)

    def isLeaf(self):
        '''Tests whether self has any subordinate requirements
        '''
        return False
class CWVTerm(models.Model):
    subjects = models.ManyToManyField("CWVSubject")
    subject_data_set = models.ManyToManyField("CWVSubjectData")
    
    def __init__(self, season, year, subject_data=None):
        '''
        Constructor
        '''

        if subject_data is None:
            subject_data = dict()

        self.dependants = dict()

        self.season = season
        self.year = year


        self.SEASON_LIST = [ "iap", "spring", "summer", "fall"]


        self.subject_data = subject_data #Key: Value = Subject : (Req, set of Msets)


    def __eq__(self, other):
        return str.lower(self.season) == str.lower(other.season) and self.year == other.year and self.subject_data == other.subject_data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        key = (self.season, self.year, frozenset(self.getSubjects()))
        return hash(key)

    def __lt__(self, other):
        if self.year == other.year:
            return self.SEASON_LIST.index(str.lower(self.season)) < self.SEASON_LIST.index(str.lower(other.season))
        else:
            return self.year < other.year

    def matches_time_of(self, other_term):
        return str.lower(self.season) == str.lower(other_term.season) and self.year == other_term.year #and self.subject_msets == other.subject_msets and self.subject_reqs == other.subject_reqs


    def getReq(self, subj):
        '''Takes a subject and returns the requirement paired with that subject this term
        '''
        if subj in self.subject_data:
            return self.subject_data[subj][0]
        else:
            return CWVRequirement()

    def get_subject_by_name(self, string):
        '''Returns a subject that has a name matching string
        '''
        #this could be sped up a lot
        try:
            for subj in self.getSubjects():
                if subj == CWVSubject(string):
                    return subj
        except:
            return None


    def getSubjects(self):
        '''Returns a copied set of the term's subjects
        '''
        return set(self.subject_data.keys())

    def getMeetingSets(self, subj):
        ''' Returns a copied set of the total meetingsets used by subj  
        '''
#        msets = set(self.subject_data[subj][1])
#        print msets, self.subject_data[subj]
        return set(self.subject_data[subj][1])


    def rebuildDeps(self):
        '''sets self.dependants to a dictionary containing pairs of (subj, set(subjects that require subj))
        '''
        expanded_reqs = dict()
        for req in [data_tuple[0] for data_tuple in self.subject_data.values()]:
            expanded_reqs[req] = req.expand(self)

        for subj in self.getSubjects():
            for required_subject in expanded_reqs[self.getReq(subj)].getSubjects():
                if required_subject not in self.dependants:
                    self.dependants[required_subject] = set()
                self.dependants[required_subject].add(subj)


    def addSubject(self, subj, req, msets=None):
        if msets is None:
            msets = set()
            msets.add(CWVMeetingSet())
        self.subject_data[subj] = (req, msets)


    def removeSubject(self, subj):
        del self.subject_data[subj]


    def addMeetingSet(self, subj, mset):
        msets = self.getMeetingSets(subj)
        msets.add(mset)
        self.subject_data[subj] = (self.getReq(subj), msets,)

    def removeMeetingSet(self, subj, mset):
        msets = self.getMeetingSets(subj)
        msets.remove(mset)
        self.subject_data[subj] = (self.getReq(subj), msets,)

    def setReq(self, subj, newReq):

        self.subject_data[subj] = (newReq, self.getMeetingSets(subj),)

    def isValidTerm(self):
        try:
            subject_msets = reduce(lambda x, y: x.extend(y), [tuple[1] for tuple in self.subject_data.values()], [])
            return hasattr(self, "subject_data") and reduce(lambda x, y : x and y.isValidMset(), subject_msets, True)
        except:
            return False

    def hasSubject(self, subject):
        return subject in self.subject_data.keys()
    
class CWVSubjectReqChoice(models.Model):
    coursePlan = models.ForeignKey("CWVCoursePlan")
    subject = models.ForeignKey("CWVSubject")
    requirement = models.ForeignKey("CWVRequirement")
    
class CWVSubjectData(models.Model):
    term = models.ForeignKey("CWVTerm")
    subject = models.ForeignKey("CWVSubject")
    requirement = models.ForeignKey("CWVRequirement")
    meetingsets = models.ManyToManyField("CWVMeetingset")