'''
Created on Nov 20, 2010

@author: richard
'''

from courser.ReqTotal import ReqTotal
from courser.Requirement import Requirement

class ReqSingleSubject(Requirement):
    '''
    classdocs
    '''


    def __init__(self, subj=None, name="unnamed requirement"):
        '''
        Constructor
        '''

        self.singleSubject = subj
        self.name = name

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
                return ReqTotal([self, subject_req.expand(term)])

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

    def __repr__(self):
        return "<Require subject: " + str(self.singleSubject) + ">"
    
    def to_json(self):
        return {"__class__": "ReqSingleSubject",
                "singleSubject": self.singleSubject,
                "name": self.name,
                }
