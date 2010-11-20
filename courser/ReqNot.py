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
    
    def __repr__(self):
        return "<ReqNot: " + str(self.reqForNegation)+ ">"
    
