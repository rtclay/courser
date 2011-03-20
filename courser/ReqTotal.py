'''
Created on Nov 22, 2010

@author: richard
'''
from courser.ReqPartial import ReqPartial

class ReqTotal(ReqPartial):
    '''
    classdocs
    '''


    '''
    classdocs
    '''


    def __init__(self, reqList=[], name="unnamed requirement"):
        '''
        Constructor
        '''
        self.reqs = reqList
        self.numNeeded = len(self.reqs)
        self.name = name

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
        return reduce(lambda x, y: x + y.isSatisfied(classesTaken), self.reqs, 0) >= self.numNeeded

    def expand(self, term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''
        #the req has multiple subreqs
        return ReqTotal([req.expand(term) for req in self.reqs])

    def squish(self):
        '''Returns a new requirement that has empty shells stripped away        
        '''

        self.testValidity()
        if not self.reqs:
            return self


        if len(self.reqs) == 1 and self.numNeeded == 1:
            return self.reqs[0].squish()

        newReq = ReqTotal(self.reqs[:])
        #Note: because it iterates on self.reqs and removes from a copy, there is no longer the problem of deleting from an iterating sequence 
        for subreq in self.reqs:
            if hasattr(subreq, "reqs") and bool(subreq.reqs) & (subreq.numNeeded == len(subreq.reqs)):
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

    def __repr__(self):
        return "<Req: all of " + str(self.getNumChoices()) + ":" + str(sorted(self.reqs, key=lambda x : x.getSingleSubj)) + ">"

    def to_json(self):
        return {"__class__": "ReqTotal",
                "reqs": self.reqs,
                "numNeeded": self.numNeeded,
                "name": self.name,
                }
