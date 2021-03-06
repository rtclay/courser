'''
Created on Aug 17, 2010

@author: richard
'''
from courser.Catalog import Catalog, TermMissingError
from courser.Requirement import Requirement, SatisfactionError
from courser.SemesterPlan import SemesterPlan
from itertools import izip, combinations, chain, imap
from random import sample
import sys




class CoursePlan(object):
    '''
    A CoursePlan contains information about a possible route to a goal.
    The CoursePlan does not directly store a Requirement as a goal.
    Instead, it stores a set of Subjects that are desired to be taken.
    SolveReq takes a Requirement and returns a set of Subjects that solve that Requirement.
    The Courseplan has a SemesterPlan for each Term in its Catalog.
    
    member data:
    desired = set()    Contains subjects that the Courseplan wants to take.
    catalog = Catalog()
    subjects_credited = set()    Contains subjects that start out having been passed, eg passing 18.01 with AP math credit
    __depths = dict()  Memoizes the depths of classes.  It is reset every time a search is requested, in order that it remain current
    term_info_dict = dict()    Matches a term to a semester plan
    subject_scores = dict()    Matches a term to a dictionary.  That dictionary matches a subject to a score, used as a heuristic for deciding routes
    subject_req_choices = dict()    Matches a Requirement to a completely expanded, total Requirement. 
    
    '''


    def __init__(self, desired=None, catalog=Catalog(), subject_req_choices=None):
        '''
        Constructor
        '''
        if desired is None:
            self.desired = set()
        else:
            self.desired = set(desired)
        if subject_req_choices is None:
            subject_req_choices = dict()
        self.subject_req_choices = subject_req_choices


        self.catalog = catalog
        self.breadth = 10
        self.maxSubjectsPerTerm = 5
        self.minUnits = 36
        self.maxUnits = self.maxSubjectsPerTerm * 12
        self.searchDepth = 1
        self.semesterPlanLimit = 6000
        self.subjects_credited = set() #this is for classes that start out having been passed, eg passing 18.01 with AP math credit
        self.__depths = dict()  #this is a dictionary that memoizes the depths of classes.  it is reset every time a search is requested, in order that it remain current

        self.term_info_dict = dict(zip(catalog.getTerms(), map(SemesterPlan, catalog.getTerms()))) #key = term, value = sem_plan

        self.subject_scores = dict()
        for trm in self.catalog.getTerms():
            self.subject_scores[trm] = dict()

    def __eq__(self, other):
        try:
            truth = True
            truth = truth and self.desired <= other.desired and self.desired >= other.desired
            truth = truth and self.term_info_dict == other.term_info_dict
            truth = truth and self.catalog == other.catalog
            return  truth
        except:
            return False

    def __hash__(self):
        key = (self.desired, self.term_info_dict, self.catalog)
        return hash(key)

    def __ne__(self, other):
        return not self.__eq__(other)


    def staticScoreSemesterPlan(self, sem_plan):
        """ Return a number that represents the heuristic value of a SemesterPlan
         towards completing the desired set of subjects.
        Does not consider future semesters
        """
        term = sem_plan.getTerm()
        value = len(sem_plan.desired)
        for subj in sem_plan.desired:
            value = value + self.scoreSubject(subj, term)

        if not sem_plan.getSolution():
            value = value - 10000
        if sem_plan.getUnits() < self.minUnits:
            value = value * 0.15
        if sem_plan.getUnits() > self.maxUnits:
            value = value * 0.15

        if set(sem_plan.getSubjects()) == set(self.getSubjectsRemaining(sem_plan.getTerm())):
            value = value + 1000

        return value

    def getDesired(self):
        """Return a set containing the Subjects desired to be taken.
        """
        return self.desired.copy()
    def setDesired(self, newDesired):
        """Define the desired Subjects to be taken.
        """
        self.desired = set(newDesired)

    def getSubjectsRemaining(self, term):
        '''Return the complete set of Subjects that are desired but not yet taken at the time of term.
        '''
        return self.desired ^ self.getSubjectsTakenBeforeTerm(term)

    def getSubjectsTakenBeforeTerm(self, term):
        '''Return the complete set of Subjects that have been taken before the start of a given term.
        '''
        set_of_subjects = self.subjects_credited.copy()

        previous_terms = self.catalog.getPreviousTerms(term)

        #get the subjects of the semester plans associated with each term in the catalog's previous terms
        for t in previous_terms:
            set_of_subjects |= self.term_info_dict[t].getSubjects()
        return set_of_subjects

    def solveReq(self, req, term):
        '''Return a solution to a requirement, returning the same solution each time for partial Requirements.
        The solution is a fully expanded requirement that has been traced out to single subject Requirements.
        '''
        req.testValidity()
        req = req.completeSquish()
        if req.__repr__() in self.subject_req_choices:
            solution = self.subject_req_choices[req.__repr__()]
        else:

            if req.isLeaf():
                if term.getReq(req.getSingleSubj()) == Requirement():
                    solution = req

                else:
                    pre_requirements = req.expand(term)
                    pre_requirements.removeReq(req)

                    solution = Requirement([req, self.solveReq(pre_requirements, term)], 2)
            elif req.isTotal():
                solution_components = [self.solveReq(sub_req, term) for sub_req in req.getReqs()]
                unique_components = list(set(solution_components))
                num_duplicates = len(solution_components) - len(unique_components)
                #print "num dup is ", num_duplicates
                solution = Requirement(unique_components, req.numNeeded - num_duplicates)
            #In this case, req is a partial requirement 
            else:
                solution_components = [self.solveReq(sub_req, term) for sub_req in sample(req.getReqs(), req.numNeeded)]
                unique_components = list(set(solution_components))
                num_duplicates = len(solution_components) - len(unique_components)
                solution = Requirement(unique_components, req.numNeeded - num_duplicates)

            solution = solution.completeSquish()
            solution.testValidity()
            #print "solution is ", solution
            self.subject_req_choices[req.__repr__()] = solution

        #print "RETURNING ", solution 
        return solution

    def setSolChoice(self, req, req_solution):
        """Define the expanded, total Requirement that satisfies req in the Courseplan's subject_req_choices dictionary 
        """
        self.subject_req_choices[req] = req_solution


    def getGoodSolution(self, req, term):
        '''Return a Requirement that represents one possible, complete solution of req, based on the subject requirements in term.
        This function assumes that req in the final term will accept as a solution the solution of req listed in the given term.
        
        Repeated calls of this function return either the same solution or a different solution.
        This function repeatedly searches for satisfactory reqs and picks the one that requires the fewest Terms to complete.
        '''

        print "Finding a good solution",
        minimum = self.catalog.getTerms()[-1]  #set as our starting point the final semester in catalog; all solutions will score better or equal to final semester

        best_solution_group = self.solveReq(req, term)

        #arbitrary number of repetitions
        for x in xrange(10):

            temp_cplan = CoursePlan([], self.catalog)
            possible_subject_group = temp_cplan.solveReq(req, term)
            temp_cplan.desired = possible_subject_group.getSubjects()

            temp_cplan.plotRemainingSemesters(term, 16)
            finish_term = temp_cplan.getTermOfSatisfaction()

            if finish_term is not None and (finish_term < minimum):
                best_solution_group = possible_subject_group
                minimum = finish_term
                print '!',
            else:
                print '.',

        if not best_solution_group is None:
            return best_solution_group
        else:
            raise SatisfactionError(req)



    def buildASP(self, term):
        '''Return the semesters possible for this term, and their scores.
        Returns an iterator consisting of (plan, static score of plan) pairs.
        The semesters include all possible combinations of subjects, up to the courseplan's maximum subjects per semester
        Subjects are included iff: the subject is available in the term, the subject's requirements are met, and the subject is desired 
        '''

        is_avail = lambda subj: subj in term.getSubjects() and term.getReq(subj).isSatisfied(self.getSubjectsTakenBeforeTerm(term))
        eligible_subjects = filter(is_avail , set(self.getSubjectsRemaining(term)))

        subject_combinations = chain.from_iterable(combinations(eligible_subjects, r) for r in xrange(1, self.maxSubjectsPerTerm + 1)) #iterator contains (,), (subject1,), (subject2,), (subject1, subject2,) ...


        combs = list(subject_combinations)
        s_plans = [SemesterPlan(term, list(subjects)) for subjects in combs]
        return izip(s_plans, imap(self.staticScoreSemesterPlan, s_plans))



    def plotRemainingSemesters(self, starting_term, num_semesters=10):
        '''Fill in self.term_info_dict by matching each term with the best semester plan for that term
        
        Return nothing
        '''

        if num_semesters > 0:
            self.term_info_dict[starting_term] = self.getPlanForTerm(starting_term, self.searchDepth)
            try:
                self.plotRemainingSemesters(self.catalog.getNextTerm(starting_term), num_semesters - 1)
            except TermMissingError as err:
                print "Catalog has run out of terms before reaching the desired number of semesters"

    def getTermOfSatisfaction(self, req=None):
        '''Return the first term after which all desired classes have been taken, or None if no term is found
        If req is provided, then this function returns the first term that satisfies req, or None if no term is found
        '''
        if req is not None:
            subjects_taken = set()
            for term, sem_plan in sorted(self.term_info_dict.items()):
                subjects_taken |= sem_plan.getSubjects()
                if req.isSatisfied(subjects_taken):
                    return term
        else:
            subjects_taken = set()

            for term, sem_plan in sorted(self.term_info_dict.items()):
                subjects_taken |= self.getSubjectsTakenBeforeTerm(term)
#                print len(subjects_taken), subjects_taken
#                print len(self.desired), self.desired

                if self.desired <= subjects_taken:

                    return term
        return None

    def getPlanForTerm(self, term, depth):
        '''Return a semester plan that is judged to be the best for the given term
        '''
        all_semester_plans = list(self.buildASP(term))

        if not self.desired:
            return SemesterPlan(term, [])

        if not all_semester_plans:
            return SemesterPlan(term, [])


        #if the semester plan is solvable, then it will have a score greater than 0
        for (sem_plan, score) in [x for x in all_semester_plans if x[1] > 0]:
            score = self.deepScoreSemesterPlan(sem_plan, depth, term)



        try:
            best_sem_plan_tuple = max(all_semester_plans, key=lambda sem_plan : sem_plan[1])
        except ValueError():
            print "Error finding highest-scoring semester. Returning a semester with no classes."
            return SemesterPlan(term, [])
        
        #return the score
        return best_sem_plan_tuple[0]


    def getDependents(self, term):
        '''Return a dictionary containing pairs of (subj, set(subjects that require subj))
        '''
        deps = dict()
        for subj in term.getSubjects():
            req = self.solveReq(term.getReq(subj), term)
            for req_subject in req.getSubjects():
                if req_subject not in deps:
                    deps[req_subject] = set()
                deps[req_subject].add(subj)
        return deps

    def scoreSubject(self, subj, term):
        """Return a score that can be used to decide how important a Subject is to a CoursePlan
        """
        if subj in self.subject_scores[term]:
            return self.subject_scores[term][subj]
        else:
            deps = self.getDependents(term)

            if not subj in deps:
                deps[subj] = set()
            score = 1
            score = score + 2 * len(deps[subj]) #This class is a precursor to other classes
            score = score + 10 * len(deps[subj] & self.desired)  #this class is a relevant precursor to what we want

            self.subject_scores[term][subj] = score
            return score


    def __getDepthofSubject(self, subj, term):
        '''Returns the depth of a subject
        The depth is the layer of subjects needing to be taken before the subj can be taken
        do not call this function except with careful understanding of the self.__depth dictionary
        '''
        req = term.getReq(subj)
        depth = sys.maxint

        if subj in self.__depths:
            return self.__depths[subj]
        elif subj in self.getSubjectsTakenBeforeTerm(term):
            depth = 0
        elif req.isLeaf():
            single_subj = req.getSingleSubj()
            depth = 1 + self.__getDepthofSubject(single_subj, term)
        elif req.isTotal():
            depth = 1 + max([self.__getDepthofSubject(x, term) for x in req.expand(term)])
        elif req.isBlank():
            depth = 1

        elif req.isPartial():
            options = [x.expand(term).getSubjects() for x in req.getReqs()]
            option_depths = [max([self.__getDepthofSubject(subject, term) for subject in option_group]) for option_group in options]
            depth = 1 + max(sorted(option_depths)[:req.getNumNeeded()])

        self.__depths[subj] = depth
        return depth


    def deepScoreSemesterPlan(self, sem_plan, depth, currentTerm):
        """ Return a number that represents the heuristic value of a SemesterPlan
         towards completing the desired set of subjects.
        Considers future semesters
        """
        static_score = self.staticScoreSemesterPlan(sem_plan)

        if depth <= 0:
            return static_score
        else:
            #in order to have the course plan consider the next semester, we need to tell it that it has taken the courses in the possible semplan for this semester
            #we save the list of subjects credited.  we NEED to revert to it before exiting function
            real_credits = self.subjects_credited.copy()

            #find the subjects that would remain after taking this semester plan
            remainingSubjects = set(sem_plan.getSubjects()) ^ set(self.getSubjectsRemaining(currentTerm))

            #generate and score the semester plans that could immediately follow this semester plan
            self.subjects_credited |= sem_plan.getSubjects()
            sem_planScores = self.buildASP(self.catalog.getNextTerm(currentTerm))

            if list(sem_planScores) == []:
                self.subjects_credited = real_credits
                return static_score


            bestChildSP = max(sem_planScores, key=lambda sp : sem_planScores[sp])
            deep_score = self.deepScoreSemesterPlan(bestChildSP, depth - 1, self.catalog.getNextTerm(currentTerm), remainingSubjects)

            self.subjects_credited = real_credits
            return static_score + deep_score

    def __repr__(self):
        response = "<Course Plan: "
        response = response + '\n   Satisfied in : %s \n' % str(self.getTermOfSatisfaction())

        response = response + '\n   Semester Plans:\n'
        for (x, y) in sorted(self.term_info_dict.items(), key=lambda tuple: tuple[0]):
            response = response + "    " + str(x) + " : " + str(y.getSubjects()) + '\n'
        response = response + ">"
        return response

    def to_json(self):
        return {"__class__": "CoursePlan",
            "desired": list(self.desired),
            "subject_req_choices": self.subject_req_choices,
            "catalog": self.catalog,
            "breadth": self.breadth,
            "maxSubjectsPerTerm": self.maxSubjectsPerTerm,
            "minUnits": self.minUnits,
            "maxUnits": self.maxUnits,
            "searchDepth": self.searchDepth,
            "semesterPlanLimit": self.semesterPlanLimit,
            "subjects_credited": self.subjects_credited,
            "term_info_dict": self.term_info_dict,
            "subject_scores": self.subject_scores
            }
