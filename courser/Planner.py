'''
Created on Aug 20, 2010

@author: richard
'''


from courser.Catalog import Catalog
from courser.CoursePlan import CoursePlan
from courserTests.Dataset import Dataset





#===============================================================================
# def parseReqString(input, term):
#    req = Requirement([], 1, None)
#    if input.contains(";"):
#        mandatoryComponents = input.split(";")
#    
#    for component in mandatoryComponents:
#        for subj in component.split(","):
#            req.addSubject(term.getSubject()) 
#    return Requirement(parseReqString(input), numNeeded, subj, name)
#===============================================================================

def binom(n, m):
    b = [0] * (n + 1)
    b[0] = 1
    for i in xrange(1, n + 1):
        b[i] = 1
        j = i - 1
        while j > 0:
            b[j] += b[j - 1]
            j -= 1
    return b[m]




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
            print "l, list    enter dataset browser"
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
    
    #===========================================================================
    # a=[]
    # for x in xrange(10):
    #    a.extend(dset.reqs63.getSolution(dset.terms[0]).getSubjects())
    #    #print str(len(a))+ " " +str(sorted(a))
    #    
    # for subj in set(a):
    #    countDict[subj] = a.count(subj)
    # for subj in sorted(countDict.items()):
    #    print subj
    # 
    # 
    # for item in [x for x in dset.terms[0].subjects.values() if dset.terms[0].getReq(x) == Requirement() and x in dset.AUSubjects]:
    #    print str(item)
    #    
    # print "***"
    # print len(set(dset.subjects))
    # print len(dset.subjects)
    # print Subject("6.111") in dset.subjects and Subject("6.111") in dset.AUSubjects
    # 
    
    # 
    #===========================================================================
    


    #===========================================================================
    # print cplan.getPlanForTerm(dset.terms[0], 0)
    # cplan.term_info_dict[dset.terms[0]] = cplan.getPlanForTerm(dset.terms[0], 0)
    # print cplan
    # 
    # print cplan.getPlanForTerm(dset.terms[2], 0) 
    # cplan.term_info_dict[dset.terms[2]] = cplan.getPlanForTerm(dset.terms[2], 0)
    # print cplan
    # 
    #===========================================================================
    
    

    #timing(dset.reqs63.getSolution, 10, dset.terms[0])
    
    