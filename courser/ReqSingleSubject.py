'''
Created on Nov 20, 2010

@author: richard
'''
from courser.Requirement import Requirement

class ReqSingleSubject(Requirement):
    '''
    classdocs
    '''


    
    def __init__(self, subj=None, name="unnamed requirement"):
        '''
        Constructor
        '''
        
        self.singleSubject=subj
        self.name = name

    def __eq__(self, other):
        try:
            return self.singleSubject == other.singleSubject
        except:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def isSatisfied(self, classesTaken):
        '''Returns T/F if self.singlesubject is in classesTaken
        '''
        return self.singleSubject in classesTaken
    
    def __repr__(self):
        return "<Require subject: " + str(self.singleSubject)+ ">"