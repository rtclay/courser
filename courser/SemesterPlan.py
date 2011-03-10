'''
Created on Aug 17, 2010

@author: richard
'''
from courser.Meetingset import Meetingset

class SemesterPlanError(Exception):
    """Base class for exceptions in this module."""
    pass

class SolutionError(SemesterPlanError):
    """Exception raised if the semester plan is unsolvable

    Attributes:
        desired -- current state of the Semester Plan's desired classes
        msg  -- explanation of the error
    """

    def __init__(self, desired, msg="Invalid Semester Plan"):
        self.desired = desired
        self.msg = msg

class SemesterPlan(object):
    '''
    classdocs
    '''

    def __init__(self, term, desired_subjects=None, reservedTimes=None):
        '''
        desired_subjects = [subject, subject, subject ...]
        '''


        if reservedTimes is None:
            reservedTimes = Meetingset()

        if desired_subjects is None:
            desired_subjects = set()



        self.desired = set(desired_subjects)
        self.term = term
        self.conflictDict = {}
        self.reservedTimes = reservedTimes

        if self.desired:
            self.fillMeetings()

    def __eq__(self, other):
        try:
            return self.desired == other.desired and self.term == other.term and self.reservedTimes == other.reservedTimes
        except:
            return False

    def __hash__(self):
        key = (frozenset(self.desired), self.term, self.reservedTimes)
        return hash(key)

    def __ne__(self, other):
        return not self.__eq__(other)

    def getSubjects(self):
        return self.desired.copy()

    def getUnits(self):
        return reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]), [subj.getUnits() for subj in self.desired])

    def getTerm(self):
        return self.term

    def removeCourse(self, course):
        if course in self.getSubjects():
            self.desired.remove(course)

    def addCourse(self, course):
        self.desired.add(course)

    def hasCourse(self, course):
        return course in self.getSubjects()


    def isValid(self):
        for subj in self.desired:
            if not self.term.hasSubject(subj):
                return False
        return True


    def findSwap(self, subjToSwapOut, desiredSubjects):
        pass


    def fillMeetings(self):
        for subj in self.getSubjects():
            self.calcConflicts(subj)

    def calcConflicts(self, subj):
        #meetingset is the key, conflicts = list of meetingsets with which this meetingset conflicts

        m_sets = self.term.getMeetingSets(subj)

        for mset in m_sets:
            #===================================================================
            # print "mset is " + str(mset)
            # print "keys is " + str(self.desired.keys()[:])
            # print "subj is " + str(subj)
            # print "keys with subj removed is " + str(self.desired.keys()[:].remove(subj))
            #===================================================================
            keys_minus_subj = self.getSubjects()
            keys_minus_subj.remove(subj)

            for otherSubj in keys_minus_subj:
                for otherMset in self.term.getMeetingSets(otherSubj):
                    if mset.isConflict(otherMset):
                        if self.conflictDict.has_key(mset):
                            self.conflictDict[mset].append(otherMset)
                            self.conflictDict[mset] = list(set(self.conflictDict[mset]))
                        else:
                            self.conflictDict[mset] = [otherMset]
                        if self.conflictDict.has_key(otherMset):
                            self.conflictDict[otherMset].append(mset)
                            self.conflictDict[otherMset] = list(set(self.conflictDict[otherMset]))
                        else:
                            self.conflictDict[otherMset] = [mset]


    def getSolution(self):
        duplicate = SemesterPlan(self.term, self.desired.copy(), Meetingset(sorted(self.reservedTimes.meetings)))
        #First, deal with immediate disqualifications
        #if there is a subject with no selectable meeting times, return a failure
        if [] in [duplicate.term.getMeetingSets(x) for x in duplicate.desired]:
            raise SolutionError(self.desired, "No meeting times")
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
                    duplicate.reservedTimes.addMeetingSet(mset)
                    solution = duplicate.getSolution()
                    if solution:
                        return solution
                    else:
                        duplicate.reservedTimes.removeMeetingSet(mset)
                        continue

            duplicate.desired.add(subj)


        return None


    def canAddMS(self, mset):
        return not self.reservedTimes.isConflict(mset)


    def __repr__(self):
        response = "<SemesterPlan"
        response = response + " " + str(self.term)
        if self.desired:
            response = response + '\n'
            for x in self.desired:
                response = response + "    " + str(x) + " meets at: " + str(self.term.getMeetingSets(x)) + '\n'
        if self.reservedTimes:
            response = response + '    Reserved:\n'
            response = response + '        ' + str(self.reservedTimes) + '\n'
        if self.conflictDict:
            response = response + '    Conflicts:\n'
        for (x, y) in self.conflictDict.items():
            response = response + "    " + str(x) + " conflicts with: " + str(y) + '\n'

        response = response + ">\n"
        return response

    def __str__(self):
        response = "<SemesterPlan"
        response = response + " " + str(self.term)
        if self.desired:
            response = response + '\n'
            for x in self.desired:
                response = response + "    " + str(x) + " meets at: " + str(self.term.getMeetingSets(x)) + '\n'
        response = response + ">"
        return response
