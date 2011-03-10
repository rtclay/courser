'''
Created on Mar 9, 2011

@author: richard
'''
from courser.Catalog import Catalog
from courser.CoursePlan import CoursePlan
from courser.Meeting import Meeting
from courser.Meetingset import Meetingset
from courser.ReqNot import ReqNot
from courser.ReqPartial import ReqPartial
from courser.ReqSingleSubject import ReqSingleSubject
from courser.ReqTotal import ReqTotal
from courser.Requirement import Requirement
from courser.SemesterPlan import SemesterPlan
from courser.Subject import Subject
from courser.Term import Term
import json

class CourserJsonEncoder(json.JSONEncoder):
    '''
    Allows Objects in the Courser package to be encoded in JSON
    '''


    def default(self, obj):
        if isinstance(obj, Subject):
            return {'__class__': 'Subject',
                    'name': obj.name,
                    'departmentCode': obj.departmentCode,
                    'course': obj.course,
                    'label': obj.label,
                    'inCharge': obj.inCharge,
                    'subjectLevel': obj.subjectLevel,
                    'totalUnits': obj.totalUnits,
                    'unitsLecture': obj.unitsLecture,
                    'unitsLab': obj.unitsLab,
                    'unitsPreparation': obj.unitsPreparation,
                    'gradeType': obj.gradeType,
                    'description': obj.description
                    }
        if isinstance(obj, Meeting):
            return {'__class__': 'Meeting',
                    'startTime': obj.startTime,
                    'endTime': obj.endTime,
                    'subject': obj.subj
                    }
        if isinstance(obj, Meetingset):
            return {'__class__': 'MeetingSet',
                    'meetings': obj.meetings
                    }
        if isinstance(obj, CoursePlan):
            return {'__class__': 'CoursePlan',
                    'desired': list(obj.desired),
                    'subject_req_choices': obj.subject_req_choices,
                    'catalog': obj.catalog,
                    'breadth': obj.breadth,
                    'maxSubjectsPerTerm': obj.maxSubjectsPerTerm,
                    'minUnits': obj.minUnits,
                    'maxUnits': obj.maxUnits,
                    'searchDepth': obj.searchDepth,
                    'semesterPlanLimit': obj.semesterPlanLimit,
                    'subjects_credited': obj.subjects_credited,
                    'term_info_dict': obj.term_info_dict,
                    'subject_scores': obj.subject_scores
                    }
        if isinstance(obj, Catalog):
            return {'__class__': 'Catalog',
                    'terms': obj.terms,
                    }

        if isinstance(obj, ReqNot):
            return {'__class__': 'ReqNot',
                    'reqForNegation': obj.reqForNegation,
                    'name': obj.name,
                    }
        if isinstance(obj, ReqPartial):
            return {'__class__': 'ReqPartial',
                    'reqs': obj.reqs,
                    'numNeeded': obj.numNeeded,
                    'name': obj.name,
                    }
        if isinstance(obj, ReqSingleSubject):
            return {'__class__': 'ReqSingleSubject',
                    'singleSubject': obj.singleSubject,
                    'name': obj.name,
                    }
        if isinstance(obj, ReqTotal):
            return {'__class__': 'ReqTotal',
                    'reqs': obj.reqs,
                    'numNeeded': obj.numNeeded,
                    'name': obj.name,
                    }
        if isinstance(obj, Requirement):
            return {'__class__': 'Requirement',
                    'reqs': obj.reqs,
                    'singleSubject': obj.singleSubject,
                    'numNeeded': obj.numNeeded,
                    'name': obj.name,
                    }
        if isinstance(obj, Term):
            return {'__class__': 'Term',
                    'dependants': obj.dependants,
                    'season': obj.season,
                    'year': obj.year,
                    'subjects': obj.subjects,
                    'subject_reqs': obj.subject_reqs,
                    'subject_msets': obj.subject_msets,
                    }
        if isinstance(obj, SemesterPlan):
            return {'__class__': 'SemesterPlan',
                    'desired': obj.desired,
                    'term': obj.term,
                    'conflictDict': obj.conflictDict,
                    'reservedTimes': obj.reservedTimes,
                    }


        raise TypeError(repr(obj) + ' is not JSON serializable')


