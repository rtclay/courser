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
    A catalog contains Terms, which then include Subjects and information about those Subjects.  The catalog has functions for selecting and manipulating Terms
    '''


    def __init__(self, terms=None):
        '''
        Set Terms to the argument passed in, or an empty dictionary
        '''
        if terms is None:
            terms = dict()

        self.terms = terms

    def __eq__(self, other):
        try:
            return self.terms == other.terms
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.terms)

    def addTerm(self, term):
        '''Add a term to the catalog's collection of Terms.
        '''
        self.terms[str(term)] = term

    def getTerms(self):
        '''Return a list containing the catalog's Terms.
        '''
        return self.terms.values()

    def getFollowingTerms(self, term):
        '''Take a term and returns a list containing all future terms in the catalog.
        '''
        return filter(lambda x : x > term, sorted(self.getTerms()))

    def getPreviousTerms(self, term):
        '''Take a term and returns a list containing all past terms in the catalog.
        '''
        return filter(lambda x : x < term, sorted(self.getTerms()))

    def removeTerm(self, term):
        '''Remove a Term from the catalog's list of Terms.
        '''
        del self.terms[str(term)]

    def getNextTerm(self, term):
        '''Return the Term immediately following the term given as an argument.
        Return None if there are no Terms following the term. 
        '''
        try:
            return self.getFollowingTerms(term)[0]
        except IndexError:
            return None

    def __repr__(self):
        response = "<Catalog: "

        response = response + '\n   Terms:\n'
        for (x, y) in self.terms.items():
            response = response + "    " + str(x) + " corresponds to: " + str(y) + '\n'



        response = response + ">"
        return response

    def to_json(self):
        return {"__class__": "Catalog",
                "terms": self.terms,
                }

