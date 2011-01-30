'''
Created on Aug 20, 2010

@author: richard
'''


from courser.Catalog import Catalog
from courser.CoursePlan import CoursePlan
from courser.Student import Student
from courserTests.Dataset import Dataset
import cmd
import pickle
import sys



class Planner(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt= "Courser:"
        self.current_student = Student()
        self.dset = Dataset()
        self.dset.dataSetup()
        self.catalog = Catalog(dict(zip([str(x) for x in self.dset.terms], self.dset.terms)))
        self.cplan= CoursePlan([], self.catalog)
        self.goalReq = self.dset.reqs63
        self.startTerm = self.dset.terms[0]
    
    def help_solve(self):
        print "Solves the student's currently specified requirement"
    def do_solve(self, req):
        self.cplan.desired=self.cplan.getGoodSolution(self.goalReq, self.startTerm).getSubjects()
        self.cplan.plotRemainingSemesters(self.startTerm, 16)
        print self.cplan
        
    def help_editStudent(self):
        print "Changes details about the current student"
    def do_editStudent(self, student):
        pass
    
    def help_display(self):
        print "Displays an object"
    def do_display(self, obj):
        if obj == "": obj = raw_input("Enter Object: ")
        if obj == "student":
            print self.current_student
        if obj == "subject":
            obj = raw_input("Enter subject: ")
            found = False
            for term in self.catalog.getTerms():
                if term.hasSubject(obj):
                    print term.getSubject(obj)
                    found = True
            if not found:
                print "Subject %s not found." % (obj,)
                
    
    def help_saveStudent(self):
        print "Saves the current student to disk"
    def do_saveStudent(self, filename):
        if filename == "": filename = raw_input("Enter filename: ")
        saveFile = open(filename, 'w')
        pickle.dump(self.current_student, saveFile)
    
    def help_loadStudent(self):
        print "Loads a student from a filename "
    def do_loadStudent(self, filename):
        if filename == "": filename = raw_input("Enter filename: ")
        saveFile = open(filename, 'r')
        self.current_student= pickle.load(saveFile)
        
    
            
    
        
    def help_EOF(self):
        print "Quits the program"
    def do_EOF(self, line):
        sys.exit()


if __name__ == '__main__':
    
    planner = Planner()
    planner.cmdloop()
  
    
    