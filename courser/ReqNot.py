'''
Created on Nov 10, 2010

@author: richard
'''
from courser.Requirement import Requirement

class ReqNot(Requirement):
    '''
    classdocs
    '''
    
    def __init__(self, reqForNegation, name="unnamed requirement"):
        '''
        Constructor
        '''
        self.reqForNegation = reqForNegation        
        self.name = name

    def __eq__(self, other):
        try:
            return self.reqForNegation == other.reqForNegation
        except:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns the opposite truth value to whether self is satisfied by the classesTaken
        '''
        return not self.reqForNegation.isSatisfied(classesTaken)
    
    def expand(self,term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''
        
        #the req has multiple subreqs
        return ReqNot([req.expand(term) for req in self.reqs])
    
    def getProgress(self, classesTaken):
        if self.isSatisfied(classesTaken):
            return 1
        else:
            return 0
    def getNumChoices(self):
        return 1
    
         
    def isLeaf(self):
        '''Tests whether self has any subordinate requirements
        '''         
        return False
    def __repr__(self):
        return "<ReqNot: " + str(self.reqForNegation)+ ">"
    
