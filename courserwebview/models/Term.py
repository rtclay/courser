'''
Created on Aug 17, 2010

@author: richard
'''
from courserwebview.models import Requirement, Subject, Meetingset
from django.db import models


class Term(models.Model):
    '''
    classdocs
    '''
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
            return Requirement()

    def get_subject_by_name(self, string):
        '''Returns a subject that has a name matching string
        '''
        #this could be sped up a lot
        try:
            for subj in self.getSubjects():
                if subj == Subject(string):
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
            msets.add(Meetingset())
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

    def __repr__(self):
        response = "<Term: " + str(self.season) + str(self.year) + " " + str(len(self.getSubjects())) + " subjects"

        response = response + ">"
        return response

    def __str__(self):
        return "<Term: " + str.lower(self.season) + str(self.year) + " " + str(len(self.getSubjects())) + " subjects>"

    def to_json(self):
        '''Returns a JSON appropriate dictionary for use in rebuilding this object
        '''
        #change the sets into lists for JSON
        s_d_values = [(x, list(y)) for (x,y) in self.subject_data.values()]
        
        return {"__class__": "Term",
                "dependants": self.dependants,
                "season": self.season,
                "year": self.year,
                "subject_data_keys": self.subject_data.keys(),
                "subject_data_values": s_d_values
                }
