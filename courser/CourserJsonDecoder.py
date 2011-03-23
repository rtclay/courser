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
from courser.Student import Student

class CourserJsonDecoder(json.JSONDecoder):
    '''
    Decodes JSON into Courser objects
    '''

    def decode (self, json_object):
        # JSON can not use single quotes, so we replace ' with "
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
                            endTime=json_object_dict["endTime"]
                            )
            if json_object_dict["__class__"] == "Student":
                stud = Student(name=json_object_dict["name"],
                               ID=json_object_dict["student_id"]
                            )
                stud.setGoals(self.decode(json_object_dict["goals"].__str__().replace("'", '"').replace("None", "null")))
                stud.setSubjects_taken(self.decode(json_object_dict["subjects_taken"].__str__().replace("'", '"').replace("None", "null")))
                #stud.setCourse_plan(self.decode(json_object_dict["course_plan"].__str__().replace("'", '"').replace("None", "null")))
                return stud
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

                term_list = [self.decode(x.__str__().replace("'", '"').replace("None", "null")) for x in json_object_dict["terms"].values]

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
                              subj=singlesubj,
                              name=json_object_dict["name"]
                            )
            if json_object_dict["__class__"] == "Term":
                #these are Subjects
                subj_data_keys = [self.decode(x.__str__().replace("'", '"').replace("None", "null")) for x in json_object_dict["subject_data_keys"]]
                #acquire lists of Requirements and [MeetingSet] from tuples of (Requirement, [Meetingset])
                subj_data_reqs, subj_data_mset_lists = zip(*[(self.decode(req.__str__().replace("'", '"').replace("None", "null")), [self.decode(mset.__str__().replace("'", '"').replace("None", "null")) for mset in mset_list]) for req , mset_list in json_object_dict["subject_data_values"]])



#                print "Keys: ", subj_data_keys
#                print "Reqs: ", subj_data_reqs
#                print "mset lists: ", subj_data_mset_lists
                # zip up req and list of msets into a tuple, then zip up Subject and that tuple into another tuple, then make a dictionary of it
                subj_data = dict(zip(subj_data_keys, zip(subj_data_reqs , subj_data_mset_lists)))


                term = Term(season=json_object_dict["season"],
                              year=json_object_dict["year"],
                              subject_data=subj_data
                            )
                term.dependants = json_object_dict["dependants"]
                return term


            if json_object_dict["__class__"] == "SemesterPlan":
                desired = [self.decode(x.__str__().replace("'", '"').replace("None", "null")) for x in json_object_dict["desired"]]
                reserved = self.decode(json_object_dict["reserved_times"].__str__().replace("'", '"').replace("None", "null"))
                trm = self.decode(json_object_dict["term"].__str__().replace("'", '"').replace("None", "null"))
                plan = SemesterPlan(term=trm,
                              desired_subjects=desired,
                              reserved_times=reserved,
                            )
                keys = [self.decode(x.__str__().replace("'", '"').replace("None", "null")) for x in json_object_dict["conflict_dict_keys"]]
                values = [self.decode(x.__str__().replace("'", '"').replace("None", "null")) for x in json_object_dict["conflict_dict_values"]]

                plan.conflict_dict = dict(zip(keys, values))
                return plan
        return json_object
