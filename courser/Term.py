'''
Created on Aug 17, 2010

@author: richard
'''
from courser.Requirement import Requirement
from courser.Subject import Subject
from courser.Meetingset import Meetingset

class Term(object):
    '''
    classdocs
    '''


    def __init__(self, season, year, reqs = None, subjects = None, subject_reqs = None, subject_msets = None):
        '''
        Constructor
        '''
        if reqs is None:
            reqs = set()
        if subjects is None:
            subjects = dict()
        if subject_msets is None:
            subject_msets = dict()
        if subject_reqs is None:
            subject_reqs = dict()
            
        self.dependants = dict()    
        
        self.season = season
        self.year = year
        self.metaRequirementList = reqs
        
        self.SEASON_LIST = [ "iap", "spring", "summer", "fall"]


        self.subjects = subjects #String representations of subjects are Keys, subjects are values
        self.subject_reqs = subject_reqs #subjects are Keys, requirements are values
        self.subject_msets = subject_msets #subjects are Keys, values are lists of meetingsets
        for subj in self.subjects.values():
            if subj not in self.subject_msets:
                self.subject_msets[subj] = set([Meetingset()])
            if subj not in self.subject_reqs:
                self.subject_reqs[subj] = Requirement()
                     
        
    def __eq__(self, other):
        return str.lower(self.season) == str.lower(other.season) and self.year == other.year #and self.metaRequirementList == other.metaRequirementList and self.subject_msets == other.subject_msets and self.subject_reqs == other.subject_reqs
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        key = (self.season, self.year)
        return hash(key)
    
    def __lt__(self, other): 
        if self.year == other.year:
            return self.SEASON_LIST.index(str.lower(self.season)) < self.SEASON_LIST.index(str.lower(other.season))
        else:
            return self.year < other.year
        
    def getReq(self, subj):
        '''Takes a subject and returns the requirement paired with that subject this term
        '''
        try:
            return self.subject_reqs[subj]
        except:
            return Requirement()
    
    def getSubjects(self):
        '''Returns a copied set of the term's subjects
        '''
        return set(self.subjects.values()) 
    
    def getMeetingSets(self, subj):
        ''' Returns a copied set of the total meetingsets used by subj  
        '''
        if subj in self.subject_msets:
            return set(self.subject_msets[subj])
        else:
            msets = set()
            msets.add(Meetingset())
            return msets
    
    def rebuildDeps(self):
        '''sets self.dependants to a dictionary containing pairs of (subj, set(subjects that require subj))
        '''        
        expanded_reqs = dict()
        for req in self.subject_reqs:
            expanded_reqs[req] = req.expand(self)
        
        for subj in self.getSubjects():
            for required_subject in expanded_reqs[self.getReq(subj)].getSubjects():
                if required_subject not in self.dependants:
                    self.dependants[required_subject] = set()
                self.dependants[required_subject].add(subj)
        
        
    def addSubject(self, subj, req, msets):
        self.subjects[subj.name] = subj
        self.subject_reqs[subj] = req
        self.subject_msets[subj] = msets
#        for required_subject in req.expand(self).getSubjects():
#            if required_subject not in self.dependants:
#                self.dependants[required_subject] = set()
#            self.dependants[required_subject].add(subj)
        
    
    def removeSubject(self, subj):
#        for required_subject in self.subject_reqs[subj].expand(self).getSubjects():
#            if required_subject in self.dependants:
#                self.dependants[required_subject].remove(subj)
        del self.subjects[subj.name]
        del self.subject_reqs[subj]
        del self.subject_msets[subj]
        
        
    def addMeetingSet(self, subj, mset):
        self.subject_msets[subj].append(mset)
        
    def removeMeetingSet(self, subj, mset):
        self.subject_msets[subj].remove(mset)
    
    def setReq(self, subj, newReq):
        self.subject_reqs[subj] = newReq
        
    def isValid(self):
        return len(self.subject_msets)== len(self.subject_reqs)
    
    def copyTerm(self, otherTerm):
        self.subjects = otherTerm.subjects.items()
        self.subject_reqs = otherTerm.subject_reqs.items()
        self.subject_msets = otherTerm.subject_msets.items()
        self.metaRequirementList = otherTerm.metaRequirementList
    
    def hasSubject(self, subject):
        return subject in self.subjects.values()
    
    
    
    def __repr__(self):
        response ="<Term: "+ str(self.season)+ str(self.year)+" "+str(len(self.subjects))+" subjects"
        
        #=======================================================================
        # response = response + '\n   SubjectMsets:\n' 
        # for (x, y) in self.subject_msets.items():
        #    response = response +"    "+ str(x) + " meets at: " + str(y) + '\n'
        # response = response + '   SubjectReqs:\n'
        # for (x, y) in self.subject_reqs.items():
        #        response = response +"    "+ str(x) + " requires " + str(y) + '\n'
        #=======================================================================

        
        response = response + ">"
        return response
    
    def __str__(self):
        return "<Term: " + str.lower(self.season)+ str(self.year)+" "+str(len(self.subjects))+" subjects>"