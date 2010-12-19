'''
Created on Aug 20, 2010

@author: richard
'''


from courser.Catalog import Catalog
from courser.CoursePlan import CoursePlan
from courserTests.Dataset import Dataset




if __name__ == '__main__':
    
    loop = True
    dset = Dataset()
    dset.dataSetup()
    catalog= Catalog(dict(zip([str(x) for x in dset.terms], dset.terms)))
    
    cplan = CoursePlan([], catalog)

    goalReq = dset.reqs63
    startTerm = dset.terms[0]
    
    input ='h'
    
    while loop:
        if input == "h":
            print "h, help    print this help message"
            #print "l, list    enter dataset browser"
            print "s, solve    solve the selected requirement"
            print "q, quit    quit the program"
        elif input == "s":
            cplan.desired=cplan.getGoodSolution(goalReq, startTerm).getSubjects()
            cplan.plotRemainingSemesters(startTerm, 16)
            
            print cplan
        elif input == "q":
            loop = False
            break;
        input = raw_input("--> ")
        
    print "program ended"
  
    
    