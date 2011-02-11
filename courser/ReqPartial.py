'''
Created on Nov 20, 2010

@author: richard
'''
from courser.Requirement import Requirement

class ReqPartial(Requirement):
    '''
    classdocs
    '''


    def __init__(self, reqList=[], numNeeded=0, name="unnamed requirement"):
        '''
        Constructor
        '''
        self.reqs = reqList
        self.numNeeded = numNeeded
        self.name = name

    def __eq__(self, other):
        try:
            return self.getReqs() == other.getReqs() and self.numNeeded == other.numNeeded
        except:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def getSubjects(self):
        subjects = []
        for req in self.reqs:
            subjects.extend(req.getSubjects())
        
        return set(subjects)
    
    def getNumChoices(self):
        return len(self.reqs)
    
    def getProgress(self, classesTaken):    
        #return the progress of its constituent requirements
        return reduce(lambda x, y: x+y.getProgress(classesTaken), self.reqs, 0)

    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns whether enough component requirements have been satisfied
        '''
        return reduce(lambda x, y: x+y.isSatisfied(classesTaken), self.reqs, 0) >= self.numNeeded
    
    def expand(self,term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''
        #the req has multiple subreqs
        return ReqPartial([req.expand(term) for req in self.reqs], self.numNeeded)
    
    def getComplexity(self, term):
        return 1.5 * reduce(lambda x, y: x+y.getComplexity(term), self.reqs, 0) 
    
    def isLeaf(self):
        '''Tests whether self has any subordinate requirements
        '''         
        return False
    
    
    
    def __repr__(self):
        return "<Req: " + str(self.numNeeded)+ " of " + str(self.getNumChoices())+":"+ str(sorted(self.reqs, key = lambda x : x.getSingleSubj)) +">"