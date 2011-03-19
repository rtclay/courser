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

class CourserJsonDecoder(json.JSONDecoder):
    '''
    Decodes JSON into Courser objects
    '''

    def decode (self, json_object):
#        print "---"
#        print "Trying to load: ", json_object.__class__.__name__, json_object        
        json_object_dict = json.loads(json_object)
        #print "still ok"
        if "__class__" in json_object_dict:
            if json_object_dict["__class__"] == "Subject":
                return Subject(name=json_object_dict["name"],
                            departmentcode=json_object_dict["departmentCode"],
                            course=json_object_dict["course"],
                            label=json_object_dict["label"],
                            incharge=json_object_dict["inCharge"],
                            subjectLevel=json_object_dict["subjectLevel"],
                            totalUnits=json_object_dict["totalUnits"],
                            unitsLecture=json_object_dict["unitsLecture"],
                            unitsLab=json_object_dict["unitsLab"],
                            unitsPreparation=json_object_dict["unitsPreparation"],
                            gradeType=json_object_dict["gradeType"],
                            description=json_object_dict["description"]
                            )
            if json_object_dict["__class__"] == "Meeting":
                return Meeting(startTime=json_object_dict["startTime"],
                            endTime=json_object_dict["endTime"],
                            # JSON can not use single quotes, so we replace ' with "
                            subj=self.decode(json_object_dict["subject"].__str__().replace("'", '"'))
                            )
            if json_object_dict["__class__"] == "MeetingSet":
                meeting_strings = [self.decode(x.__str__().replace("'", '"')) for x in json_object_dict["meetings"]]

                return Meetingset(meetings=meeting_strings)
            if json_object_dict["__class__"] == "CoursePlan":
                plan = CoursePlan(desired=json_object_dict["desired"],
                            catalog=json_object_dict["catalog"],
                            subject_req_choices=json_object_dict["subject_req_choices"]
                            )
                plan.subjects_credited = json_object_dict["subjects_credited"]
                plan.term_info_dict = json_object_dict["term_info_dict"]
                plan.subject_scores = json_object_dict["subject_scores"]
                return plan
            if json_object_dict["__class__"] == "Catalog":
                print json_object_dict["terms"].__class__.__name__
                print  "dict is ", json_object_dict["terms"]

                for x, y in json_object_dict["terms"].items():
                    print x, " ---- ", y
                term_list = json_object_dict["terms"].keys()
                print term_list
                cat = Catalog(terms=term_list)
                return cat
            if json_object_dict["__class__"] == "ReqNot":
                return ReqNot(reqForNegation=json_object_dict["reqForNegation"],
                              name=json_object_dict["name"]
                            )
            if json_object_dict["__class__"] == "ReqPartial":
                return ReqPartial(reqs=json_object_dict["reqs"],
                              numNeeded=json_object_dict["numNeeded"],
                              name=json_object_dict["name"]
                            )
            if json_object_dict["__class__"] == "ReqTotal":
                return ReqTotal(reqs=json_object_dict["reqs"],
                              numNeeded=json_object_dict["numNeeded"],
                              name=json_object_dict["name"]
                            )
            if json_object_dict["__class__"] == "ReqSingleSubject":
                subj = json_object_dict["singleSubject"]
                return ReqSingleSubject(subj=self.decode(subj.__str__().replace("'", '"').replace("None", "null")),
                              name=json_object_dict["name"]
                            )
            if json_object_dict["__class__"] == "Requirement":
                requirements = [self.decode(x.__str__().replace("'", '"').replace("None", "null")) for x in json_object_dict["reqs"]]
                
                if json_object_dict["singleSubject"] is None:
                    singlesubj = None
                else:
                    singlesubj = self.decode(json_object_dict["singleSubject"].__str__().replace("'", '"'))
                
                return Requirement(reqs=requirements,
                              numNeeded=json_object_dict["numNeeded"],
                              subj= singlesubj,
                              name=json_object_dict["name"]
                            )
            if json_object_dict["__class__"] == "Term":

                subj_data_keys = [self.decode(x.__str__().replace("'", '"').replace("None", "null")) for x in json_object_dict["subject_data_keys"]]
                subj_data_values = [self.decode(x.__str__().replace("'", '"').replace("None", "null")) for x in json_object_dict["subject_data_values"]]
                subj_data = dict(zip(subj_data_keys, subj_data_values))
                

                term = Term(season=json_object_dict["season"],
                              year=json_object_dict["year"],
                              subject_data = subj_data
                            )
                term.dependants = json_object_dict["dependants"]
                return term
            if json_object_dict["__class__"] == "SemesterPlan":
                plan = SemesterPlan(term=json_object_dict["season"],
                              desired_subjects=json_object_dict["desired"],
                              reservedTimes=json_object_dict["reservedTimes"],
                              subject_reqs=json_object_dict["subject_reqs"],
                            )
                plan.conflictDict = json_object_dict["conflictDict"]
                return term
        return json_object
