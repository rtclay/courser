'''
Created on Aug 18, 2010

@author: richard
'''
from random import sample



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
        self.msg = msg + req.__str__()



class Requirement(object):
    '''
    classdocs
    '''


    def __init__(self, reqList=[], numNeeded=0, subj=None, name="unnamed requirement"):
        '''
        Constructor
        '''
        self.reqs = reqList
        self.singleSubject = subj
        self.numNeeded = numNeeded
        self.name = name
        
    def __iter__(self):
        for n in self.reqs:
            if (isinstance(n, Requirement)):            
                yield n
                
    def __eq__(self, other):
        return self.reqs == other.reqs and self.singleSubject == other.singleSubject and self.numNeeded == other.numNeeded
    
    def __ne__(self, other):
        return not self.__eq__(other)        
        
        
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
        if not self.reqs:
            return self
        
        
        if len(self.reqs)== 1 and self.numNeeded==1:
            return self.reqs[0].squish()
        
        newReq = Requirement(self.reqs[:], self.numNeeded, self.singleSubject)
        #Note: because it iterates on self.reqs and removes from a copy, there is no longer the problem of deleting from a iterating sequence 
        for subreq in self.reqs:
            if bool(subreq.reqs) & (subreq.numNeeded == len(subreq.reqs)):
                for subsubreq in subreq:
                    newReq.addReq(subsubreq.squish())
                newReq.removeReq(subreq)
        return newReq
    
    def completeSquish(self):
        temp = Requirement(self.reqs[:], self.numNeeded, self.singleSubject)
        while temp != temp.squish():
            temp = temp.squish()
        return temp
            

    def expand(self,term):
        '''Returns a req with each subject traced out to subjects with no req 
        
        Returns a Requirement that includes the prerequisite subjects of every subject in self's reqs.  Almost certain to include duplicate subjects and reqs.
        '''
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
        
             
    #returns one possible solution to the requirement, choosing randomly in instances where a choice (eg 3 out of 4) is available
    def subsolve(self):
        '''Returns a random Requirement that represents one possible, complete solution of self, based on the subject requirements in term
        '''
        newFlatReq = Requirement(self.reqs, self.numNeeded, self.singleSubject)
        if newFlatReq.isLeaf():
            return newFlatReq
        if newFlatReq.isTotal():
            return Requirement([req.subsolve() for req in newFlatReq.reqs], newFlatReq.numNeeded)
            
        if newFlatReq.isValid() and not newFlatReq.isTotal():
            return Requirement(list(set([req.subsolve() for req in sample(newFlatReq.reqs, newFlatReq.numNeeded)])), newFlatReq.numNeeded)

        else:
            raise SatisfactionError(newFlatReq)
    

    def getSolution(self, term):
        '''Returns a Requirement that represents one possible, complete solution of self, based on the subject requirements in term
        
        Repeated calls of this function result in pseudorandom requirements that satisfy self
        '''
        a = self.expand(term).subsolve()
        while a != a.squish():
            a = a.squish()
        
        return a

             
    def getSubjects(self):
        if self.singleSubject:
            return [self.singleSubject]
        else:
            subjects = []
            for req in self.reqs:
                subjects.extend(req.getSubjects())
            
            return set(subjects)
            
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
    
    def isValid(self):
        
        if not (self.getNumChoices() >= 0) & (self.numNeeded <= self.getNumChoices()):
            print self.getNumChoices()
            print self.numNeeded
        
        return (self.getNumChoices() >= 0) & (self.numNeeded <= self.getNumChoices())
    
    def testValidity(self):
        if not self.isValid():
            raise MalformedReqError(self)
        
    def isLeaf(self):
        '''Tests whether self has any subordinate requirements
        '''         
        return not self.reqs
    
    def isTotal(self):
        '''Tests whether the top level of this requirement requires all of its components to be satisfied
        '''
        if self.isLeaf():
            return True
        else:
            return (self.numNeeded == self.getNumChoices())
    
    def isBlank(self):
        return (self.numNeeded == 0)&(self.singleSubject == None)
        
    def __repr__(self):
        if self.isLeaf():
            return "<Req: "+ str(self.singleSubject)+">"
        else:
            return "<Req: " + str(self.numNeeded)+ " of " + str(self.getNumChoices())+":"+ str(sorted(self.reqs, key = lambda x : x.getSingleSubj)) +">"