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


    def __init__(self, season, year, reqs=[], subjects = None, subjectReqs=None, subjectMsets=None):
        '''
        Constructor
        '''
        if subjects is None:
            subjects= dict()
        if subjectMsets is None:
            subjectMsets= dict()
        if subjectReqs is None:
            subjectReqs= dict()    
        
        self.season= season
        self.year = year
        self.metaRequirementList= reqs
        
        self.SEASON_LIST= [ "iap", "spring", "summer", "fall"]

        self.subjects = subjects #String representations of subjects are Keys, subjects are values
        self.subjectReqs = subjectReqs #subjects are Keys, requirements are values
        self.subjectMsets = subjectMsets #subjects are Keys, values are lists of meetingsets
        for subj in self.subjects.values():
            if subj not in self.subjectMsets:
                self.subjectMsets[subj] = [Meetingset()]
            if subj not in self.subjectReqs:
                self.subjectReqs[subj] = Requirement()
                     
        
    def __eq__(self, other):
        return str.lower(self.season) == str.lower(other.season) and self.year == other.year #and self.metaRequirementList == other.metaRequirementList and self.subjectMsets == other.subjectMsets and self.subjectReqs == other.subjectReqs
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other): 
        if self.year == other.year:
            return self.SEASON_LIST.index(str.lower(self.season)) < self.SEASON_LIST.index(str.lower(other.season))
        else:
            return self.year < other.year
        
    def getReq(self, subj):
        '''Takes a subject and returns the requirement paired with that subject this term
        '''
        try:
            return self.subjectReqs[subj]
        except:
            return Requirement()
    
    def getSubjects(self):
        '''Returns a copied list of the term's subjects
        '''
        return self.subjects.values()[:] 
    
    def getMeetingSets(self, subj):
        ''' Returns a copied list of the total meetingsets used by subj  
        '''
        if subj in self.subjectMsets:
            return self.subjectMsets[subj][:]
        else:
            return [Meetingset()]
        
    def addSubject(self, subj, req, msets, altSubjectName=""):
        if subj is None:
            subj= Subject(altSubjectName)
        self.subjects[subj.name] = subj
        self.subjectReqs[subj] = req
        self.subjectMsets[subj] = msets
    
    def removeSubject(self, subj, altSubjectName=""):
        if subj is None:
            subj= Subject(altSubjectName)
        del self.subjects[subj.name]
        del self.subjectReqs[subj]
        del self.subjectMsets[subj]
        
    def addMeetingSet(self, subj, mset):
        self.subjectMsets[subj].append(mset)
        
    def removeMeetingSet(self, subj, mset):
        self.subjectMsets[subj].remove(mset)
    
    def setReq(self, subj, newReq):
        self.subjectReqs[subj] = newReq
        
    def isValid(self):
        return len(self.subjectMsets)== len(self.subjectReqs)
    
    def copyTerm(self, otherTerm):
        self.subjects= otherTerm.subjects.items()
        self.subjectReqs= otherTerm.subjectReqs.items()
        self.subjectMsets= otherTerm.subjectMsets.items()
        self.metaRequirementList= otherTerm.metaRequirementList
    
    def hasSubject(self, subject):
        return subject in self.subjects.values()
    
    
    
    def __repr__(self):
        response ="<Term: "+ str(self.season)+ str(self.year)+" "+str(len(self.subjects))+" subjects"
        
        #=======================================================================
        # response = response + '\n   SubjectMsets:\n' 
        # for (x, y) in self.subjectMsets.items():
        #    response = response +"    "+ str(x) + " meets at: " + str(y) + '\n'
        # response = response + '   SubjectReqs:\n'
        # for (x, y) in self.subjectReqs.items():
        #        response = response +"    "+ str(x) + " requires " + str(y) + '\n'
        #=======================================================================

        
        response = response + ">"
        return response
    
    def __str__(self):
        return "<Term: " + str.lower(self.season)+ str(self.year)+" "+str(len(self.subjects))+" subjects>"