'''
Created on Mar 9, 2011

@author: richard
'''
from courser.Catalog import Catalog
from courser.CoursePlan import CoursePlan
from courser.CourserJsonEncoder import CourserJsonEncoder
from courser.Subject import Subject
from courserTests.Dataset import Dataset
import json
from courser.CourserJsonDecoder import CourserJsonDecoder

dset = Dataset()
dset.dataSetup()
catalog = Catalog(dict(zip([str(x) for x in dset.terms], dset.terms)))
cplan = CoursePlan([], catalog)
goalReq = dset.reqs63
startTerm = dset.terms[0]

print cplan
a= Subject("A")
string = json.dumps(a, cls = CourserJsonEncoder)
print string
print json.loads(string)
b = json.loads(string, cls= CourserJsonDecoder)

print a, b
print a == b


#print json.dumps(cplan, cls = CourserJsonEncoder,  encoding = 'utf-8')