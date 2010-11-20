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
            return self.reqs == other.reqs and self.numNeeded == other.numNeeded
        except:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def getSubjects(self):
        subjects = []
        for req in self.reqs:
            subjects.extend(req.getSubjects())
        
        return set(subjects)

    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns whether enough component requirements have been satisfied
        '''
        return reduce(lambda x, y: x+y.isSatisfied(classesTaken), self.reqs, 0) >= self.numNeeded
    
    def __repr__(self):
        return "<Req: " + str(self.numNeeded)+ " of " + str(self.getNumChoices())+":"+ str(sorted(self.reqs, key = lambda x : x.getSingleSubj)) +">"