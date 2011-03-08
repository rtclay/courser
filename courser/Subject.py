'''
Created on Aug 18, 2010
 
@author: richard
'''

class Subject(object):
    '''
    All of the information about classes that are liable to change from year to year (instructor, meeting times, requirements) are going to be stored in Term.
    '''


    def __init__(self, name, departmentcode = "", course=0, label="", incharge="no one", subjectLevel = "undergraduate", totalUnits=12, unitsLecture =4, unitsLab=4, unitsPreparation =4, gradeType="", description = ""):
        '''
        Constructor
        '''
        self.name = name
        self.departmentCode = departmentcode
        self.course = course
        self.label = label
        self.inCharge = incharge
        self.subjectLevel = subjectLevel
        self.totalUnits = totalUnits
        self.unitsLecture = unitsLecture
        self.unitsLab = unitsLab
        self.unitsPreparation = unitsPreparation
                
        self.gradeType = gradeType
        self.description = description
        
    def __lt__(self, other):
        return self.name < other.name
        
    
    def __eq__(self, other):
        if other and self:
            return self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return "<Subject: " + str(self.name)+ ">"
        
    def getUnits(self):
        return (self.unitsLecture, self.unitsLab, self.unitsPreparation)
    