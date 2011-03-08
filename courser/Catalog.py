'''
Created on Aug 18, 2010

@author: richard
'''
from Term import Term



class CatalogError(Exception):
    """Base class for exceptions in this module."""
    pass

class TermMissingError(CatalogError):

    def __init__(self, term):
        self.term = term
        self.msg = "Term %s not contained in catalog" % term
        
        
    def __repr__(self):
        return self.msg
        
class Catalog(object):
    '''
    classdocs
    '''


    def __init__(self, terms=None):
        '''
        Constructor
        '''
        if terms is None:
            terms = dict()
          
        self.terms= terms
        
    def __eq__(self, other):       
        try:
            return self.terms == other.terms
        except:
            return False
        
    def __hash__(self):
        return hash(self.terms)    
        
    def addTerm(self, term):
        self.terms[str(term)] = term
        
    def getTerms(self):
        return self.terms.values()
    
    def getFollowingTerms(self, term):
        '''Takes a term and returns a list containing all future terms in the catalog
        '''
        return filter(lambda x : x > term, sorted(self.terms.values())) 
    
    def getPreviousTerms(self, term):
        '''Takes a term and returns a list containing all past terms in the catalog
        '''
        return filter(lambda x : x < term, sorted(self.terms.values()))    
    
    def removeTerm(self,term):
        del self.terms[str(term)]

    def getNextTerm(self, term):
        return self.getFollowingTerms(term)[0]
    
    


            
    def __repr__(self):
        response ="<Catalog: "
        
        response = response + '\n   Terms:\n' 
        for (x, y) in self.terms.items():
            response = response +"    "+ str(x) + " corresponds to: " + str(y) + '\n'
        

        
        response = response + ">"
        return response
    
    
        