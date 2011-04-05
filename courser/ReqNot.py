'''
Created on Nov 10, 2010

@author: richard
'''
from courser.Requirement import Requirement

class ReqNot(Requirement):
    '''
    A ReqNot is a type of Requirement that contains a single subsidiary requirement.
    Its primary difference is that ReqNot returns True for isSatisfied for a given set of subjects IFF the subsidiary requirement returns false.
    '''

    def __init__(self, reqForNegation, name="unnamed requirement"):
        '''
        Initialize reqForNegation.  It must be a Requirement or subclass.
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

    def __hash__(self):
        key = (self.reqForNegation)
        return hash(key)

    def isSatisfied(self, classesTaken):
        '''Take a list of subjects and return the opposite truth value 
        to whether the subsidiary requirement is satisfied.
        '''
        return not self.reqForNegation.isSatisfied(classesTaken)

    def expand(self, term):
        '''Return a req with each subject traced out to subjects with no req 
        
        Return a ReqNot that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''

        #the req has multiple subreqs
        return ReqNot(self.reqForNegation.expand(term))

    def getProgress(self, classesTaken):
        """Return the integer number of subsidiary requirements fulfilled.
        For a ReqNot, this will always be either 0 or 1.
        """
        if self.isSatisfied(classesTaken):
            return 1
        else:
            return 0
    def getNumChoices(self):
        """Return the integer number of subsidiary requirements.
        For a ReqNot, this will always be 1.
        """
        return 1

    def getSubjects(self):
        '''Return a set of all the subjects touched by a requirement
        '''
        return set()

    def getComplexity(self, term):
        '''CURRENTLY USELESS
        Return a positive number representing the complexity of the req's subordinate requirements
        Roughly, complexity increases with the depth and number of the req's sub-requirements
        Every subreq will be less complex than its parent
        When the Requirement class becomes an interface, this function will return a notImplementedError for the Requirement Class; subclasses will define.
        '''
        #TODO: make useful
        return self.reqForNegation.getComplexity(term)

    def isLeaf(self):
        '''Test whether self has any subordinate requirements.
        '''
        return False
    def __repr__(self):
        return "<ReqNot: " + str(self.reqForNegation) + ">"
    def to_json(self):
        return {"__class__": "ReqNot",
                "reqForNegation": self.reqForNegation,
                "name": self.name,
                }
