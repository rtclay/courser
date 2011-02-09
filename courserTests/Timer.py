'''
Created on Oct 14, 2010

@author: richard
'''
from courser.Catalog import Catalog
from courser.CoursePlan import CoursePlan
from courserTests.Dataset import Dataset
import time




def timing(f, n, a):
        print f.__name__,
        r = range(n)
        t1 = time.clock()
        for i in r:
            f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a)
        t2 = time.clock()
        print round(t2-t1, 5)
        
def timing0args(f, n):
        print f.__name__,
        r = range(n)
        t1 = time.clock()
        for i in r:
            f(); f(); f(); f(); f(); f(); f(); f(); f(); f()
        t2 = time.clock()
        print round(t2-t1, 5)

def timing2args(f, n, a, b):
        print f.__name__,
        r = xrange(n)
        t1 = time.clock()
        for i in r:
            f(a, b); f(a, b); f(a, b); f(a, b); f(a, b); f(a, b); f(a, b); f(a, b); f(a, b); f(a, b)
        t2 = time.clock()
        print round(t2-t1, 5)


    

if __name__ == '__main__':
    dset = Dataset()
    dset.dataSetup()
    catalog= Catalog(dict(zip([str(x) for x in dset.terms], dset.terms)))
    

    cplan = CoursePlan([], catalog)
    
    expanded = dset.reqs63.expand(dset.terms[0])

    #===========================================================================
    # timing(dset.reqs63.expand, 10, dset.terms[0])
    # timing0args(dset.reqs63.expand(dset.terms[0]).squish, 10) 
    # timing0args(expanded.squish().subsolve, 10 )
    # 
    #===========================================================================
    
    timing2args(cplan.solveReq, 10, dset.reqs63, dset.terms[0])
    
    
    timing2args(cplan.plotRemainingSemesters, 1, dset.terms[0], 16)
    
    timing2args(cplan.getGoodSolution, 1, dset.reqs63, dset.terms[0])
    
    
    
    
