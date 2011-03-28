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

#with open('subjects.json', mode='w') as f:
#    json.dump(dset.subjects.extend(dset.AUSubjects), f, indent=2, cls = CourserJsonEncoder)
items_minus_sets = [(x, list(y[1])) for (x, y) in dset.subject_data.items()]
print items_minus_sets 
with open('subject_data.json', mode='w') as f:
    json.dump(items_minus_sets, f, indent=2, cls = CourserJsonEncoder)


#print json.dumps(cplan, cls = CourserJsonEncoder,  encoding = 'utf-8')