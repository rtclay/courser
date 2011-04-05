'''
Created on Mar 30, 2011

@author: richard
'''
from django.db import models

class Subject(models.Model):
    '''
    Subject contains information about a class being taught.
    '''
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    
    def __lt__(self, other):
        return self.name < other.name


    def __eq__(self, other):        
        try:
            return self.name == other.name
        except:
            return False

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "<Subject: " + str(self.name) + ">"

    def getUnits(self):
        return (self.unitsLecture, self.unitsLab, self.unitsPreparation)

    def isValidSubject(self):
        '''TODO: MAKE ME A REAL FUNCTION please
        '''
        return True
       
        
        