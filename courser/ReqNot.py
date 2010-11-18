'''
Created on Nov 10, 2010

@author: richard
'''
from courser.Requirement import Requirement

class ReqNot(Requirement):
    '''
    classdocs
    '''


    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns the opposite truth value to whether self is satisfied by the classesTaken
        '''
        return not super(ReqNot, self).isSatisfied()
    
