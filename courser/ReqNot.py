'''
Created on Nov 10, 2010

@author: richard
'''
from courser.Requirement import Requirement

class ReqNot(Requirement):
    '''
    classdocs
    '''
    
    def __init__(self, reqList, name="unnamed requirement"):
        '''
        Constructor
        '''
        self.reqs = reqList
        self.numNeeded = 1
        self.name = name


    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns the opposite truth value to whether self is satisfied by the classesTaken
        '''
        return not super(ReqNot, self).isSatisfied(classesTaken)
    
