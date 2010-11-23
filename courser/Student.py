'''
Created on Aug 18, 2010

@author: richard
'''
from courser.CoursePlan import CoursePlan
from courserTests.Dataset import Dataset


class Student(object):
    '''
    classdocs
    '''


    def __init__(self, name="", ID=None):
        '''
        Constructor
        '''
        self.dset = Dataset()
        self.dset.dataSetup()
        
        self.name = name
        self.student_id = ID
        self.goals = []
        self.course_plan = CoursePlan([], self.dset)

    def getDset(self):
        return self.dset


    def getName(self):
        return self.name


    def getStudent_id(self):
        return self.student_id


    def getGoals(self):
        return self.goals


    def getCourse_plan(self):
        return self.course_plan


    def getSubjects_taken(self):
        return self.subjectsTaken


    def setDset(self, value):
        self.dset = value


    def setName(self, value):
        self.name = value


    def setStudent_id(self, value):
        self.student_id = value


    def setGoals(self, value):
        self.goals = value


    def setCourse_plan(self, value):
        self.course_plan = value


    def setSubjects_taken(self, value):
        self.subjectsTaken = value


    def delDset(self):
        del self.dset


    def delName(self):
        del self.name


    def delStudent_id(self):
        del self.student_id


    def delGoals(self):
        del self.goals


    def delCoursePlan(self):
        del self.course_plan


    def delSubjectsTaken(self):
        del self.subjectsTaken

        
        
        
        
    def getProgress(self, req):
        return req.getProgress(self.subjectsTaken)
    
    def satisfiesReq(self, req):
        return req.isSatisfied(self.subjectsTaken)

    

    
        
        