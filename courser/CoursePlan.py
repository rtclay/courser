'''
Created on Aug 17, 2010

@author: richard
'''
from courser.Catalog import Catalog, TermMissingError
from courser.SemesterPlan import SemesterPlan
from itertools import izip, combinations, chain, imap
from courser.Requirement import Requirement, RequirementError, SatisfactionError
from random import sample
from test.test_codecs import all_string_encodings



class CoursePlan(object):
    '''
    classdocs
    '''


    def __init__(self, desired=None, catalog= Catalog(), subject_req_choices= None):
        '''
        Constructor
        '''
        if desired is None:
            self.desired = []
        else:
            self.desired = desired
        if subject_req_choices is None:
            subject_req_choices= dict()
        self.subject_req_choices= subject_req_choices      
            
        #self.req = req
        
        
        self.catalog = catalog
        self.breadth = 10
        self.maxSubjectsPerTerm = 5
        self.minUnits = 36
        self.maxUnits = self.maxSubjectsPerTerm*12
        self.searchDepth = 1
        self.semesterPlanLimit= 6000
        self.subjects_credited = [] #this is for classes that start out having been passed, eg passing 18.01 with AP math credit
        
        
        self.term_info_dict = dict(zip(catalog.getTerms(), map(SemesterPlan, catalog.getTerms()))) #key = term, value = sem_plan
    
    def staticScoreSemesterPlan(self, sem_plan):
        value = len(sem_plan.desired)
        if not sem_plan.getSolution():
            value = value -1000
        if sem_plan.getUnits() < self.minUnits:
            value = value * 0.75
        if sem_plan.getUnits() > self.maxUnits:
            value = value * 0.75
        
        if set(sem_plan.getSubjects()) == set(self.getSubjectsRemaining(sem_plan.getTerm())):
            value = value +1000    
        
        return value
    
    def getDesired(self):
        return list(self.desired)[:]
    
    def getSubjectsRemaining(self, term):
        '''Returns a list of Subjects that are desired but not yet taken at the time of term
        '''
        return list(set(self.desired) ^ set(self.getSubjectsTakenBeforeTerm(term)))
     
    def getSubjectsTakenBeforeTerm(self, term):
        list_of_subjects = self.subjects_credited[:]
        
        previous_terms = self.catalog.getPreviousTerms(term)

        #get the subjects of the semester plans associated with each term in the catalog's previous terms
        for t in previous_terms:
            list_of_subjects.extend(self.term_info_dict[t].getSubjects())
        return list_of_subjects
    
    def getSolChoice(self, req, term):
        #print "req is", req
        req.testValidity()
        req = req.completeSquish()
        if req.__repr__() in self.subject_req_choices:
            solution = self.subject_req_choices[req.__repr__()]
            #print "key:", str(req)
            #print "value:", str(solution) 
        else:
            #print "key not found: ", req.__repr__(), "\n", req.__repr__() in self.subject_req_choices
            #print "dict is: "
            #for x in self.subject_req_choices.items():
                #print x
            if req.isLeaf():
                if term.getReq(req.getSingleSubj()) == Requirement():
                    solution = req
                    #print req
                    
                else:                    
                    pre_requirements = req.expand(term)
                    pre_requirements.removeReq(req)
 
                    solution = Requirement([req, self.getSolChoice(pre_requirements, term)], 2)    
            elif req.isTotal():
                solution_components = [self.getSolChoice(sub_req, term) for sub_req in req.reqs]
                unique_components = list(set(solution_components))
                num_duplicates = len(solution_components) - len(unique_components)
                #print "num dup is ", num_duplicates
                solution = Requirement(unique_components, req.numNeeded-num_duplicates)
            #In this case, req is a partial requirement 
            else:
                solution_components = [self.getSolChoice(sub_req, term) for sub_req in sample(req.reqs, req.numNeeded)]
                unique_components = list(set(solution_components))
                num_duplicates = len(solution_components) - len(unique_components)
                solution = Requirement(unique_components, req.numNeeded-num_duplicates) 
                
            solution = solution.completeSquish()
            solution.testValidity() 
            #print "solution is ", solution
            self.subject_req_choices[req.__repr__()] = solution 
            
        #print "RETURNING ", solution 
        return solution
            
    def setSolChoice(self, req, req_solution): 
        self.subject_req_choices[req] = req_solution
        
    def solveReq(self, req, term): 
        '''Returns a Requirement that represents one possible, complete solution of self, based on the subject requirements in term
        
        Repeated calls of this function return the same solution
        '''
        a = self.getSolChoice(req, term)
       
        return a
    
    def getGoodSolution(self, req, term):
        '''Returns a Requirement that represents one possible, complete solution of req, based on the subject requirements in term
        
        Repeated calls of this function return the same solution
        This function repeatedly searches for satisfactory reqs and picks the one that requires the fewest classes.
        '''
        
        #self.term_info_dict.clear() # we are coming up with a new solution

        print "Finding a good solution",
        minimum = self.catalog.getTerms()[-1]

        best_solution_group = self.solveReq(req, term)
        
        
        for x in xrange(20):
            
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
                
                    
        #print "Solution found:"
        #print "Soonest to satisfy: ", str(minimum)        
        
        
        
    
    def buildASP(self, term):
        '''Returns an iterator consisting of (plan, static score of plan) pairs
        '''
        
        is_avail = lambda subj: subj in term.getSubjects() and term.getReq(subj).isSatisfied(self.getSubjectsTakenBeforeTerm(term))
        eligible_subjects = filter(is_avail , set(self.getSubjectsRemaining(term)))
        
        subject_combinations = chain.from_iterable(combinations(eligible_subjects, r) for r in xrange(1, self.maxSubjectsPerTerm+1)) #iterator contains (,), (subject1,), (subject2,), (subject1, subject2,) ...
        
        
        combs = list(subject_combinations)
        s_plans = [SemesterPlan(term, list(s)) for s in combs]
        return izip(s_plans, imap(self.staticScoreSemesterPlan, s_plans))

    

    def plotRemainingSemesters(self, starting_term, num_semesters=10):
        '''Fills in self.term_info_dict
        
        Returns nothing
        '''
        
        if num_semesters >0:
            self.term_info_dict[starting_term]= self.getPlanForTerm(starting_term, self.searchDepth)
            try:
                self.plotRemainingSemesters(self.catalog.getNextTerm(starting_term), num_semesters-1)
            except TermMissingError as err:
                print "Catalog has run out of terms before reaching the desired number of semesters"
 
    def getTermOfSatisfaction(self, req=None):
        '''Returns the first term after which all desired classes have been taken, or None if no term is found
        If req is provided, then this function returns the first term that satisfies req, or None if no term is found
        '''
        if req is not None:
            subjects_taken = []
            for term, sem_plan in sorted(self.term_info_dict.items()):
                subjects_taken.extend(sem_plan.getSubjects())
                if req.isSatisfied(subjects_taken):
                    return term
        else:
            #Note: this loop has n^2 performance n=number terms
            for term in sorted(self.term_info_dict.keys()):
                if self.getSubjectsRemaining(term) == []:
                    return term
            return None
    
    def getPlanForTerm(self, term, depth):
        '''Returns a semester plan that is judged to be the best for the given term
        '''
        all_semester_plans = list(self.buildASP(term))
        
        if not self.desired:
            return SemesterPlan(term, [])
        
        if not all_semester_plans:
            return SemesterPlan(term, [])

        #=======================================================================
        # for (sem_plan, score) in [x for x in all_semester_plans if x[1] > 0]:
        #    score = self.deepScoreSemesterPlan(sem_plan, depth, term)
        #=======================================================================

        
        try:
            best_sem_plan_tuple = max(all_semester_plans, key = lambda sem_plan : sem_plan[1])            
        except ValueError():
            print "Error finding highest-scoring semester. Returning a semester with no classes."
            return SemesterPlan(term)
 
        return best_sem_plan_tuple[0]

            
        

        

    def deepScoreSemesterPlan(self, sem_plan, depth, currentTerm):
        if depth <= 0:
            return self.staticScoreSemesterPlan(sem_plan)
        else:
            #find the subjects that would remain after taking this semester plan
            remainingSubjects = set(sem_plan.getSubjects()) ^  set(self.getSubjectsRemaining(currentTerm))
            #generate and score the semester plans that could immediately follow this semester plan
            sem_planScores = self.buildASP(self.catalog.getNextTerm(currentTerm))
            
            bestChildSP = max(sem_planScores, key = lambda sp : sem_planScores[sp])
            
            return self.staticScoreSemesterPlan(sem_plan)+self.deepScoreSemesterPlan(bestChildSP, depth-1, self.catalog.getNextTerm(currentTerm), remainingSubjects)
    
    def __repr__(self):
        response ="<Course Plan: "
        response = response + '\n   Satisfied in : %s \n' % str(self.getTermOfSatisfaction())
        
        response = response + '\n   Semester Plans:\n' 
        for (x, y) in sorted(self.term_info_dict.items(), key = lambda tuple: tuple[0]):
            response = response +"    "+ str(x) +" : "+str(y.getSubjects())+ '\n'
        response= response+">"
        return response