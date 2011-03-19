'''
Created on Aug 18, 2010

@author: richard
'''
from random import sample
import copy




class RequirementError(Exception):
    """Base class for exceptions in this module."""
    pass

class SatisfactionError(RequirementError):
    """Exception raised if the Requirement cannot be satisfied

    Attributes:
        req -- current state of the Requirement
        msg  -- explanation of the error
    """

    def __init__(self, req, msg="Cannot satisfy requirement"):
        self.req = req
        self.msg = msg + req.__str__()
        
class MalformedReqError(RequirementError):
    """Exception raised if the Requirement is somehow malformed, eg requiring 4 of 3 options

    Attributes:
        req -- current state of the Requirement
        msg  -- explanation of the error
    """

    def __init__(self, req, msg="Malformed Requirement"):
        self.req = req
        self.msg = msg +" "+ req.__class__.__name__+" "+ str(req.__dict__)
    def __str__(self):
        return repr(self.msg)



class Requirement(object):
    '''
    classdocs
    TODO: transform req into an abstract class or interface and force the use of its subclasses.  Remove all instantiations of Requirement class from project
    '''


    def __init__(self, reqs=None, numNeeded=0, subj=None, name="unnamed requirement"):
        '''
        Constructor
        '''
        if reqs is None:
            reqs = []
        self.reqs = []
        
        for item in reqs:            
            if hasattr(item, "isValidReq") and item.isValidReq():
                self.reqs.append(item)
                continue
            elif hasattr(item, "isValidSubject") and item.isValidSubject():
                self.reqs.append(Requirement([], 1, subj = item ))
                continue
            else:
                raise MalformedReqError(item)
        
        
        
        self.singleSubject = subj
        self.numNeeded = numNeeded
        self.name = name
        self.testValidity()
        
    def __iter__(self):
        for n in self.reqs:
            if (isinstance(n, Requirement)):            
                yield n
                
    def __eq__(self, other):
        try:
            return self.reqs == other.reqs and self.singleSubject == other.singleSubject and self.numNeeded == other.numNeeded
        except:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)        
        
    def __hash__(self):
        key = (frozenset(self.reqs), self.singleSubject, self.numNeeded)
        return hash(key)
        
    def isSatisfied(self, classesTaken):
        '''Takes a list of classes taken and returns True or False according to whether the req is satisfied
        '''
        if self.isLeaf():
            if self.singleSubject is None:
                return True
            else:
                return self.singleSubject in classesTaken
        else:
            return reduce(lambda x, y: x+y.isSatisfied(classesTaken), self.reqs, 0) >= self.numNeeded

    def getNumNeeded(self):
        return self.numNeeded
    
    def getReqs(self):
        '''Returns a set containing the requirement's subrequirements
        Returns an empty set if there are no subrequirements
        '''
        if self.reqs:
            return self.reqs
        else:
            return set()
        
    def setReqs(self, set_of_Reqs):
        self.reqs = set_of_Reqs
    
    def getNumChoices(self):
        if self.isLeaf():
            if self.singleSubject is None:
                return 0
            else:
                return 1 #the single subject presents one choice
        else:        
            return len(self.reqs)
    
    def addSubject(self, subject):
        #if the subject isnt already in the top layer of requirements, add a new leaf req to self's list containing the subj
        if not(subject in [x.getSingleSubj for x in self.reqs]):
            self.numNeeded +=1
            self.reqs.append(Requirement(subj= subject))
            
    def addReq(self, req):
        #if the subject isnt already in the top layer of requirements, add the req to self's reqs
        if not(req in self.reqs):
            self.numNeeded= self.numNeeded+1
            self.reqs.append(req)
            
    def removeReq(self, req):
        if req in self.reqs:
            self.reqs.remove(req)
            self.numNeeded= self.numNeeded-1
            
    def generateReq(self, listOfSubjects, numNeeded):
        listOfReqs = []

        for subj in listOfSubjects:
            listOfReqs.append(Requirement([], 0, subj))
        return Requirement(listOfReqs, numNeeded, subj)

      
    def squish(self):
        '''Returns a new requirement that has empty shells stripped away        
        '''
        
        self.testValidity()
        if not self.reqs:
            return self
        
        
        if len(self.reqs)== 1 and self.numNeeded==1:
            return self.reqs[0].squish()
        
        newReq = Requirement(self.reqs[:], self.numNeeded, self.singleSubject)
        #Note: because it iterates on self.reqs and removes from a copy, there is no longer the problem of deleting from an iterating sequence 
        for subreq in self.reqs:
            if hasattr(subreq, "reqs") and bool(subreq.reqs) & (subreq.numNeeded == len(subreq.reqs)):
                for subsubreq in subreq:
                    newReq.addReq(subsubreq.squish())
                newReq.removeReq(subreq)
        return newReq
    
    def completeSquish(self):
        temp = copy.copy(self)
        #temp = Requirement(self.reqs[:], self.numNeeded, self.singleSubject)
        while temp != temp.squish():
            temp = temp.squish()
        return temp
            

    def expand(self,term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''
        if self.isBlank():
            return self
        #if it doesn't have sub requirements, just look at the single subject
        if not self.reqs:
            #if it is an empty requirement, return self
            if self.singleSubject is None:
                return self
            #if the req has a single subject, expand that subject
            subject_req = term.getReq(self.singleSubject) 
            
            if subject_req.isBlank():
                #if self's single subject has a blank requirement, return self
                return self
            else:
                return Requirement([self, subject_req.expand(term)], 2) 
        
        
        #in this case, the req has multiple subreqs
        return Requirement([req.expand(term) for req in self.reqs], self.numNeeded) 
        

             
    def getSubjects(self):
        '''Returns a set of all the subjects touched by a requirement
        '''
        subjects = set()
        if self.isLeaf():
            subjects.add(self.singleSubject)           
        else:            
            for req in self.reqs:
                subjects |= req.getSubjects()
                            
        return subjects
            
    def getSingleSubj(self):
        return self.singleSubject        

    def getProgress(self, classesTaken):
        if self.isLeaf():
            if self.singleSubject in classesTaken:
                return 1
            else:
                return 0
        else:
            #return the progress of its constituent requirements
            return reduce(lambda x, y: x+y.getProgress(classesTaken), self.reqs, 0)
    
    def isValidReq(self):
        try:
            for req in self.reqs:
                if not req.isValidReq():
                    return False
            
            if not (self.getNumChoices() >= 0) & (self.numNeeded <= self.getNumChoices()):
                print self.getNumChoices()
                print self.numNeeded
            
            return (self.getNumChoices() >= 0) & (self.numNeeded <= self.getNumChoices())
        except:
            return False
    
    def testValidity(self):
        if not self.isValidReq():
            raise MalformedReqError(self)
        
    def getComplexity(self, term):
        '''Returns a positive number representing the complexity of the req's subordinate requirements
        Roughly, complexity increases with the depth and number of the req's sub-requirements
        Every subreq will be less complex than its parent
        When the Requirement class becomes an interface, this function will return a notImplementedError for the Requirement Class; subclasses will define.
        '''

        return 1.5 * reduce(lambda x, y: x+y.getComplexity(term), self.reqs, 0) + int(self.isLeaf()) 
        
    def isLeaf(self):
        '''Tests whether self has any subordinate requirements
        '''         
        return not self.reqs
    
    def isTotal(self):
        '''Tests whether the top level of this requirement requires all of its components to be satisfied
        Returns True IFF self is a leaf or self.numNeeded == self.getNumChoices()
        '''
        if self.isLeaf():
            return True
        else:
            return (self.numNeeded == self.getNumChoices())
    def isPartial(self):
        '''Tests whether the top level of this requirement requires only part of its components to be satisfied
        Returns True IFF self.numNeeded != self.getNumChoices()
        '''
        return (self.numNeeded != self.getNumChoices())
    
    def isBlank(self):
        return (self.numNeeded == 0)&(self.singleSubject == None)
        
    def __repr__(self):
        if self.isLeaf():
            return "<Req: "+ str(self.singleSubject)+">"
        else:
            return "<Req: " + str(self.numNeeded)+ " of " + str(self.getNumChoices())+":"+ str(sorted(self.reqs, key = lambda x : x.getSingleSubj)) +">"
    def to_json(self):
        return {"__class__": "Requirement",
                "reqs": self.reqs,
                "singleSubject": self.singleSubject,
                "numNeeded": self.numNeeded,
                "name": self.name,
                }    
    