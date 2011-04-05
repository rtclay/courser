'''
Created on Mar 30, 2011

@author: richard
'''
from django.db import models

class Person(models.Model):
    '''
    A person model represents a person: instructor, student etc
    '''
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


       
        
        