'''
Created on Aug 18, 2010

@author: richard
'''


class Student(object):
    '''
    classdocs
    '''


    def __init__(self, goals =[], subjectsTaken =[], coursePlan=None, reqsMet={}):
        '''
        Constructor
        '''
        self.goals = goals
        self.subjectsTaken = subjectsTaken
        self.coursePlan = coursePlan
        self.reqsMet = reqsMet
        
    def getProgress(self, req):
        return req.getProgress(self.subjectsTaken)
    
    def satisfiesReq(self, req):
        return req.isSatisfied(self.subjectsTaken)
    
    def takeClass(self, subject):
        self.subjectsTaken.append(subject)
    
        
        