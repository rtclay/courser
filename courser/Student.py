'''
Created on Aug 18, 2010

@author: richard
'''
from courser.CoursePlan import CoursePlan
from courserTests.Dataset import Dataset
from courser.ReqSingleSubject import ReqSingleSubject
from courser.ReqTotal import ReqTotal
from courser.ReqNot import ReqNot


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
        self.course_plan = CoursePlan([], self.dset.catalog)

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

   
        
        
    def getProgress(self, req):
        return req.getProgress(self.subjectsTaken)
    
    def satisfiesReq(self, req):
        return req.isSatisfied(self.subjectsTaken)
    
    def avoid_Subject(self, subject):        
        self.goals = ReqTotal([self.goals, ReqNot(ReqSingleSubject(subject))]) 

    def __repr__(self):
        return "<Student: " + str(self.name)+ ">"
        