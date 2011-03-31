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

    def __init__(self, term, desired_subjects=None, reserved_times=None):
        '''
        desired_subjects = [subject, subject, subject ...]
        '''


        if reserved_times is None:
            reserved_times = Meetingset()

        if desired_subjects is None:
            desired_subjects = set()


        self.desired = set(desired_subjects)
        self.term = term
        self.conflict_dict = {}
        self.reserved_times = reserved_times

#        print "reserved: ", self.reserved_times

        if self.desired:
            self.fillMeetings()

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


    def fillMeetings(self):
        for subj in self.getSubjects():
            self.calcConflicts(subj)

    def calcConflicts(self, subj):
        #meetingset is the key, conflicts = list of meetingsets with which this meetingset conflicts

        m_sets = self.term.getMeetingSets(subj)
#        print "msets: ", m_sets

        for mset in m_sets:
            #===================================================================
            # print "mset is " + str(mset)
            # print "keys is " + str(self.desired.keys()[:])
            # print "subj is " + str(subj)
            # print "keys with subj removed is " + str(self.desired.keys()[:].remove(subj))
            #===================================================================
            keys_minus_subj = self.getSubjects()
            keys_minus_subj.remove(subj)
#            print mset, mset.__class__.__name__, mset.isValidMset()

            for otherSubj in keys_minus_subj:
                for otherMset in self.term.getMeetingSets(otherSubj):
                    if mset.isConflict(otherMset):
                        if self.conflict_dict.has_key(mset):
                            self.conflict_dict[mset].append(otherMset)
                            self.conflict_dict[mset] = list(set(self.conflict_dict[mset]))
                        else:
                            self.conflict_dict[mset] = [otherMset]
                        if self.conflict_dict.has_key(otherMset):
                            self.conflict_dict[otherMset].append(mset)
                            self.conflict_dict[otherMset] = list(set(self.conflict_dict[otherMset]))
                        else:
                            self.conflict_dict[otherMset] = [mset]


    def getSolution(self):
        duplicate = SemesterPlan(self.term, self.desired.copy(), Meetingset(sorted(self.reserved_times.meetings)))
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
                    duplicate.reserved_times.addMeetingSet(mset)
                    solution = duplicate.getSolution()
                    if solution:
                        return solution
                    else:
                        duplicate.reserved_times.removeMeetingSet(mset)
                        continue

            duplicate.desired.add(subj)


        return None


    def canAddMS(self, mset):
        return not self.reserved_times.isConflict(mset)


    def __repr__(self):
        response = "<SemesterPlan"
        response = response + " " + str(self.term)
        if self.desired:
            response = response + '\n'
            for x in self.desired:
                response = response + "    " + str(x) + " meets at: " + str(self.term.getMeetingSets(x)) + '\n'
        if self.reserved_times:
            response = response + '    Reserved:\n'
            response = response + '        ' + str(self.reserved_times) + '\n'
        if self.conflict_dict:
            response = response + '    Conflicts:\n'
        for (x, y) in self.conflict_dict.items():
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
    def to_json(self):
        return {"__class__": "SemesterPlan",
                "desired": list(self.desired),
                "term": self.term,
                "conflict_dict_keys": self.conflict_dict.keys(),
                "conflict_dict_values": self.conflict_dict.values(),
                "reserved_times": self.reserved_times,
                }
