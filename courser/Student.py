'''
Created on Aug 18, 2010

@author: richard
'''
from courser.CoursePlan import CoursePlan
from courserTests.Dataset import Dataset
from courser.ReqSingleSubject import ReqSingleSubject
from courser.ReqTotal import ReqTotal
from courser.ReqNot import ReqNot
from courser.Requirement import Requirement


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
        self.goals = Requirement() #a requirement that the student wants to meet.
        self.course_plan = CoursePlan([], self.dset.catalog)
        self.subjectsTaken = []
        
    def __eq__(self, other):
        return self.student_id == other.student_id
    
    def __hash__(self):
        key = (self.student_id)
        return hash(key)

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
        
    def addSubject_taken(self, subject_or_subjects):        
        try:
            it = iter(subject_or_subjects)
            self.subjectsTaken.extend(subject_or_subjects)
        except TypeError:
            self.subjectsTaken.append(subject_or_subjects)
        
    def getProgress(self, req):
        return req.getProgress(self.subjectsTaken)
    
    def satisfiesReq(self, req):
        return req.isSatisfied(self.subjectsTaken)
    
    def avoid_Subject(self, subject):        
        self.goals = ReqTotal([self.goals, ReqNot(ReqSingleSubject(subject))]) 

    def __repr__(self):
        return "<Student: " + str(self.name)+ ">"
        