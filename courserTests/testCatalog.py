'''
Created on Sep 16, 2010

@author: richard
'''
from courser.Catalog import Catalog
from courser.Term import Term
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        
        self.terms = [Term("FALL", 2010),
                      Term("IAP", 2011),
                      Term("SPRING", 2011),
                      Term("SUMMER", 2011),
                      Term("FALL", 2011),
                      ]
        self.catalog = Catalog(dict([(str(x), x) for x in self.terms]))


    def tearDown(self):
        del self.catalog.terms 

    def testCompare(self):
        self.assertTrue(self.terms[0]< self.terms[1], "Assert: %s < %s" % (self.terms[0], self.terms[1]))
        self.assertTrue(self.terms[1]< self.terms[2], "Assert: %s < %s" % (self.terms[1], self.terms[2]))
        self.assertTrue(self.terms[0]< self.terms[2], "Assert: %s < %s" % (self.terms[0], self.terms[2]))
        
        self.assertTrue(self.terms[1]> self.terms[0], "Assert: %s > %s" % (self.terms[1], self.terms[0]))
        self.assertTrue(self.terms[2]> self.terms[1], "Assert: %s > %s" % (self.terms[2], self.terms[1]))
        self.assertTrue(self.terms[2]> self.terms[0], "Assert: %s > %s" % (self.terms[2], self.terms[0]))



    def testGetNextTerm(self):
        self.assertEqual(self.terms[1], self.catalog.getNextTerm(self.terms[0]), "Assert: %s equals %s" % (self.terms[1], self.catalog.getNextTerm(self.terms[0])))
         
    def testGetPreviousTerms(self): 
        self.assertEqual([], self.catalog.getPreviousTerms(self.terms[0]), "Assert: %s equals %s" % ([], self.catalog.getPreviousTerms(self.terms[0])))
        self.assertEqual(self.terms[0:3], self.catalog.getPreviousTerms(self.terms[3]), "Assert: %s equals %s" % (self.terms[0:3], self.catalog.getPreviousTerms(self.terms[3])))
    
    def testGetFollowingTerms(self):
        self.assertEqual([], self.catalog.getFollowingTerms(self.terms[-1]), "Assert: %s equals %s" % ([], self.catalog.getFollowingTerms(self.terms[-1])))
        self.assertEqual(self.terms[1:], self.catalog.getFollowingTerms(self.terms[0]), "Assert: %s equals %s" % (self.terms[1:], self.catalog.getFollowingTerms(self.terms[0])))

    def testRemoveTerm(self):
        self.assertIn(self.terms[0], self.catalog.getTerms())
        self.catalog.removeTerm(self.terms[0])
        self.assertNotIn(self.terms[0], self.catalog.getTerms())
        self.assertIn(self.terms[1], self.catalog.getTerms())
        self.catalog.removeTerm(self.terms[1])
        self.assertNotIn(self.terms[1], self.catalog.getTerms())

    def testRepr(self):
        print self.catalog
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()