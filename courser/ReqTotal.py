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
