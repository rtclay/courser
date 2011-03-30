 
from django.db import models



# Create your models here.
class CWVPerson(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class CWVMeeting(models.Model):
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()
    subj = models.ForeignKey('CWVSubject')
    meeting_sets = models.ManyToManyField("CWVMeetingSet")
    

class CWVMeetingSet(models.Model):
    meetings = models.ManyToManyField("CWVMeeting")

class CWVSubject(models.Model):
    name = models.CharField(max_length=64)
    departmentCode = models.CharField(max_length=64)
    course = models.CharField(max_length=64)
    label = models.CharField(max_length=64)
    inCharge = models.CharField(max_length=64)
    subjectLevel = models.CharField(max_length=64)
    totalUnits = models.PositiveIntegerField()
    unitsLecture = models.PositiveIntegerField()
    unitsLab = models.PositiveIntegerField()
    unitsPreparation = models.PositiveIntegerField()


    gradeType = models.CharField(max_length=16)
    description = models.TextField()

class CWVCatalog(models.Model):
    pass


class CWVSemesterPlan(models.Model):
    courseplan = models.ForeignKey("CWVCoursePlan")
class CWVCoursePlan(models.Model):
    pass
class CWVRequirement(models.Model):
    numneeded = models.PositiveIntegerField()
    singleSubject = models.ForeignKey("CWVSubject")
    reqs = models.ManyToManyField("self")
    name = models.CharField(max_length=64)
class CWVReqNot(models.Model):
    reqForNegation = models.ForeignKey("self")
    name = models.CharField(max_length=64)
class CWVReqPartial(models.Model):
    numneeded = models.PositiveIntegerField()
    reqs = models.ManyToManyField("self")
    name = models.CharField(max_length=64)
class CWVReqSingleSubject(models.Model):
    singleSubject = models.ForeignKey("CWVSubject")    
    name = models.CharField(max_length=64)
class CWVReqTotal(models.Model):
    numneeded = models.PositiveIntegerField()
    reqs = models.ManyToManyField("self")
    name = models.CharField(max_length=64)
class CWVTerm(models.Model):
    catalog = models.ForeignKey("CWVCatalog")