'''
Created on Sep 27, 2010

@author: richard
'''
from courser.Meeting import Meeting
from courser.Meetingset import Meetingset
from courser.Requirement import Requirement
from courser.Subject import Subject
from courser.Term import Term
from random import randint
from courser.Catalog import Catalog



class Dataset(object):
    
    def __init__(self):
        self.subjects = None
        self.AUSubjects = None
        self.mathReq = None
        self.physReq = None
        self.introReq = None
        self.foundationReq = None
        self.headerReq = None
        self.softwareLabReq = None
        self.AUSReq = None
        self.UAPReq = None
        self.reqs63 = None
        self.terms = None
        self.catalog = None

    def dataTearDown(self):
        if self.subjects is not None:
            del self.subjects
        if self.AUSubjects is not None:
            del self.AUSubjects
        if self.mathReq is not None:
            del self.mathReq 
        if self.physReq is not None:
            del self.physReq 
        if self.introReq is not None:
            del self.introReq
        if self.foundationReq is not None:
            del self.foundationReq
        if self.headerReq is not None:
            del self.headerReq
        if self.softwareLabReq is not None:
            del self.softwareLabReq
        if self.AUSReq is not None:
            del self.AUSReq
        if self.UAPReq is not None:
            del self.UAPReq
        if self.reqs63 is not None:
            del self.reqs63
        if self.terms is not None:
            del self.terms
    

    def dataSetup(self):  
          
        self.subjects = [Subject("18.01", "01", 18, "Calculus I"),
                    Subject("18.02", "02", 18, "Calculus II"),
                    Subject("18.03", "03", 18, "Calculus III"),
                    Subject("18.06", "06", 18, "Linear Algebra"),
                    Subject("18.404"),
                    Subject("18.435"),
                    Subject("18.440", "440", 18, "unnamed"),
                    Subject("18.700", "700", 18, "Linear Algebra"),
                    Subject("2.003"),
                    Subject("3.155"),
                    Subject("6.00"),
                    Subject("6.001"),
                    Subject("6.002", "002", 6),
                    Subject("6.003", "003", 6),
                    Subject("6.004", "004", 6),
                    Subject("6.005"),
                    Subject("6.006"),
                    Subject("6.007", "007", 6),
                    Subject("6.01", "01", 6, "Introduction to EECS I"),
                    Subject("6.010"),
                    Subject("6.011"),
                    Subject("6.012", "012", 6),
                    Subject("6.013", "013", 6),
                    Subject("6.02", "02", 6, "Introduction to EECS II"),
                    Subject("6.020"),
                    Subject("6.021J"),
                    Subject("6.023J"),
                    Subject("6.024J"),
                    Subject("6.033", "033", 6),
                    Subject("6.034"),
                    Subject("6.041", "041", 6, "unnamed"),
                    Subject("6.042", "042", 6, "unnamed"),
                    Subject("6.045"),
                    Subject("6.046", "046", 6, "Advanced Algorithms"),
                    Subject("6.046J"),
                    Subject("6.047"),
                    Subject("6.050J"),
                    Subject("6.070J"),
                    Subject("6.071J"),
                    Subject("6.07J"),
                    Subject("6.100", "100", 6),
                    Subject("6.101", "101", 6),
                    Subject("6.102", "102", 6),
                    Subject("6.111"),
                    Subject("6.122J"),
                    Subject("6.131"),
                    Subject("6.141J"),
                    Subject("6.142J"),
                    Subject("6.152J"),  
                    Subject("6.161", "161", 6),
                    Subject("6.163"),
                    Subject("6.173", "173", 6),         
                    Subject("6.182"),
                    Subject("6.207J"),
                    Subject("6.241"),
                    Subject("6.243"),
                    Subject("6.256"),
                    Subject("6.263J"),
                    Subject("6.266"),
                    Subject("6.267"),
                    Subject("6.281J"),
                    Subject("6.337J"),
                    Subject("6.338J"),
                    Subject("6.345J"),
                    Subject("6.376"),
                    Subject("6.437"),
                    Subject("6.438"),
                    Subject("6.440"),
                    Subject("6.443J"),
                    Subject("6.452"),
                    Subject("6.454"),
                    Subject("6.455J"),
                    Subject("6.456"),
                    Subject("6.522J"),
                    Subject("6.524J"),
                    Subject("6.561J"),
                    Subject("6.581J"),
                    Subject("6.602"),
                    Subject("6.608J"),
                    Subject("6.621"),
                    Subject("6.717J"),
                    Subject("6.719"),
                    Subject("6.720J"),
                    Subject("6.728"),
                    Subject("6.730"),
                    Subject("6.731"),
                    Subject("6.774"),
                    Subject("6.775"),
                    Subject("6.777J"),
                    Subject("6.778J"),
                    Subject("6.780J"),
                    Subject("6.804J"),
                    Subject("6.813"),
                    Subject("6.814"),
                    Subject("6.815"),
                    Subject("6.820"),
                    Subject("6.821"),
                    Subject("6.823"),
                    Subject("6.827"),
                    Subject("6.829"),
                    Subject("6.830"),
                    Subject("6.831"),
                    Subject("6.833"),
                    Subject("6.834J"),
                    Subject("6.838"),
                    Subject("6.841J"),
                    Subject("6.842"),
                    Subject("6.845"),
                    Subject("6.849"),
                    Subject("6.850"),
                    Subject("6.851"),
                    Subject("6.852J"),
                    Subject("6.853"),
                    Subject("6.854J"),
                    Subject("6.855J"),
                    Subject("6.858"),
                    Subject("6.865"),
                    Subject("6.869"),
                    Subject("6.870"),
                    Subject("6.872J"),
                    Subject("6.873J"),
                    Subject("6.874J"),
                    Subject("6.875"),
                    Subject("6.876J"),
                    Subject("6.878J"),
                    Subject("6.891"),
                    Subject("6.892"),
                    Subject("6.893"),
                    Subject("6.894"),
                    Subject("6.895"),
                    Subject("6.896"),
                    Subject("6.897"),
                    Subject("6.898"),
                    Subject("6.902J"),
                    Subject("6.921"),
                    Subject("6.921"),
                    Subject("6.922"),
                    Subject("6.923"),
                    Subject("6.938"),
                    Subject("6.946J"),
                    Subject("6.951"),
                    Subject("6.951"),
                    Subject("6.952"),
                    Subject("6.975"),
                    Subject("6.976"),
                    Subject("6.977"),
                    Subject("6.978"),
                    Subject("6.982J"),
                    Subject("6.UAP", "UAP", 6, "Undergraduate Advanced Project"),
                    Subject("6.UAT", "UAT", 6, "Undergraduate Advanced Project"),
                    Subject("7.014"),
                    Subject("8.01", "01", 8, "Physics: Classical Mechanics"),
                    Subject("8.02", "02", 8, "Physics: E&M"),
                    Subject("2.001"),
                    Subject("2.005"),
                    Subject("2.006"),
                    Subject("2.008"),
                    Subject("20.320"),
                    Subject("20.310"),
                    Subject("15.064"),
                    Subject("9.07"),
                    Subject("18.05"),
                    Subject("16.04"),
                    Subject("14.30"),
                    Subject("6.436"),
                    Subject("6.840"),
                    Subject("6.251"),
                    Subject("6.255"),
                    Subject("18.310"),
                    ]
        
        self.AUSubjects =[
                    Subject("6.022J", "022J", 6, "Quantitative Systems Physiology"),
                    Subject("6.023J", "023J", 6, "Fields, Forces and Flows in Biological Systems"),
                    Subject("6.035", "035", 6, "Computer Language Engineering"),
                    Subject("6.045J", "045J", 6, "Automata, Computability and Complexity"),
                    Subject("6.047", "047", 6, "Computational Biology: Genomes, Networks, Evolution"),
                    Subject("6.061", "061", 6, "Introduction to Electric Power Systems"),
                    Subject("6.079", "079", 6, "Introduction to Complex Optimization (Fall 2009 only)"),
                    Subject("6.111", "111", 6, "Introductory Digital Systems Laboratory"),
                    Subject("6.115", "115", 6, "Microcomputer Project Laboratory"),
                    Subject("6.131", "131", 6, "Power Electronics Laboratory"),
                    Subject("6.142J", "142J", 6, "Robotics, Science and Systems II"),
                    Subject("6.172", "172", 6, "Performance Engineering of Software Systems"),
                    Subject("6.207", "207", 6, "Networks"),
                    Subject("6.301", "301", 6, "Solid-State Circuits"),
                    Subject("6.302", "302", 6, "Feedback Systems"),
                    Subject("6.336J", "336J", 6, "Introductory to Numerical Simulation"),
                    Subject("6.341", "341", 6, "Discrete-Time Signal Processing"),
                    Subject("6.602", "602", 6, "Fundamentals of Photonics"),
                    Subject("6.641", "641", 6, "Electromagnetic Fields, Forces, and Motion"),
                    Subject("6.701", "701", 6, "Introduction to Nanoelectronics"),
                    Subject("6.801", "801", 6, "Machine Vision"),
                    Subject("6.803", "803", 6, "The Human Intelligence Enterprise"),
                    Subject("6.804J", "804J", 6, "Computational Cognitive Science"),
                    Subject("6.805", "805", 6, "Ethics and the Law on the Electronic Frontier"),
                    Subject("6.813", "813", 6, "User Interface Design and Implementation"),
                    Subject("6.814", "814", 6, "Database Systems"),
                    Subject("6.815", "815", 6, "Digital and Computational Photography"),
                    Subject("6.825", "825", 6, "Techniques in Artificial Intelligence"),
                    Subject("6.837", "837", 6, "Computer Graphics"),
                    Subject("6.840J", "840J", 6, "Theory of Computation"),
                    Subject("6.854J", "854J", 6, "Advanced Algorithms"),
                    Subject("6.857", "857", 6, "Network and Computer Security"),
                    Subject("6.867", "867", 6, "Machine Learning"),
                    Subject("16.36", "36", 6, "Communication Systems Engineering"),
                    ]
        
        self.subjectDict = {}
        for subj in self.subjects:
            self.subjectDict[subj.name] = subj
        for subj in self.AUSubjects:
            self.subjectDict[subj.name] = subj
            
        
        
        self.terms = [Term("FALL", 2010, [], self.subjectDict),
                      Term("IAP", 2011, []),
                      Term("SPRING", 2011, [], self.subjectDict),
                      Term("SUMMER", 2011, []),
                      
                      Term("FALL", 2011, [], self.subjectDict),
                      Term("IAP", 2012, []),
                      Term("SPRING", 2012, [], self.subjectDict),
                      Term("SUMMER", 2012, []),
                      
                      Term("FALL", 2012, [], self.subjectDict),
                      Term("IAP", 2013, []),
                      Term("SPRING", 2013, [], self.subjectDict),
                      Term("SUMMER", 2013, []),
                      
                      Term("FALL", 2013, [], self.subjectDict),
                      Term("IAP", 2014, []),
                      Term("SPRING", 2014, [], self.subjectDict),
                      Term("SUMMER", 2014, []),
                      
                      Term("FALL", 2014, [], self.subjectDict),
                      Term("IAP", 2015, []),
                      Term("SPRING", 2015, [], self.subjectDict),
                      Term("SUMMER", 2015, []),
                      
                      Term("FALL", 2015, [], self.subjectDict),
                      ]
        self.catalog = Catalog(dict([(str(x), x) for x in self.terms] ))
        
        for semester in range(0, len(self.terms), 2):
            self.assignMeetings(self.terms[semester])
            self.assignReqs(self.terms[semester])
        
        
        
        
        self.mathReq = Requirement([Requirement().generateReq([self.subjectDict["18.06"],self.subjectDict["18.03"]], 1),
                                    Requirement([], 1, self.subjectDict["6.042"])
                                    ],
                              2, None, "MathReq"
                              )
        self.physReq = Requirement([], 1, self.subjectDict["8.02"], "Physics")
        # GIRphysics2 = Requirement().generateReq([self.subjectDict["8.02"], self.subjectDict["8.021"], self.subjectDict["8.022"]], 1)
        self.introReq = Requirement().generateReq([self.subjectDict["6.01"], self.subjectDict["6.02"]], 2)
        self.foundationReq = Requirement().generateReq([self.subjectDict["6.004"], self.subjectDict["6.005"], self.subjectDict["6.006"]], 3)
        self.headerReq = Requirement().generateReq([self.subjectDict["6.033"], self.subjectDict["6.034"], self.subjectDict["6.046"]], 3)
        self.softwareLabReq = Requirement([], 1, self.subjectDict["6.005"], "Software Lab")
        self.AUSReq = Requirement().generateReq(self.AUSubjects, 2)
        self.UAPReq = Requirement().generateReq([self.subjectDict["6.UAT"], self.subjectDict["6.UAP"]], 2)
        
        
        self.reqs63 = Requirement([self.mathReq, self.physReq, self.introReq, self.foundationReq, self.headerReq, self.softwareLabReq, self.AUSReq, self.UAPReq], 8, None, "6.3 Degree")

    def assignReqs(self, term):
        term.setReq(self.subjectDict["18.01"], Requirement())
        term.setReq(self.subjectDict["18.02"], Requirement([], 1, self.subjectDict["18.01"]))
        term.setReq(self.subjectDict["18.03"], Requirement([], 1, self.subjectDict["18.02"]))
        term.setReq(self.subjectDict["18.06"], Requirement([], 1, self.subjectDict["18.02"]))
        term.setReq(self.subjectDict["2.003"], Requirement().generateReq([self.subjectDict["8.01"], self.subjectDict["18.03"]], 2))
        term.setReq(self.subjectDict["6.001"], Requirement())
        term.setReq(self.subjectDict["6.01"], Requirement([], 1, self.subjectDict["8.02"]))
        term.setReq(self.subjectDict["6.02"], Requirement([Requirement().generateReq([self.subjectDict["18.06"], self.subjectDict["18.03"]], 1), Requirement([], 1, self.subjectDict["6.01"])], 2))
        term.setReq(self.subjectDict["6.002"], Requirement([Requirement().generateReq([self.subjectDict["6.01"], self.subjectDict["8.02"]], 1), Requirement([], 1, self.subjectDict["18.03"])], 2))
        term.setReq(self.subjectDict["6.003"], Requirement([], 1, self.subjectDict["6.02"]))
        term.setReq(self.subjectDict["6.004"], Requirement([], 1, self.subjectDict["6.02"]))
        term.setReq(self.subjectDict["6.005"], Requirement().generateReq([self.subjectDict["6.01"], self.subjectDict["6.042"]], 2))
        term.setReq(self.subjectDict["6.006"], Requirement().generateReq([self.subjectDict["6.01"], self.subjectDict["6.042"]], 2))
        term.setReq(self.subjectDict["6.007"], Requirement().generateReq([self.subjectDict["6.01"], self.subjectDict["18.03"]], 2))
        term.setReq(self.subjectDict["6.011"], Requirement([Requirement().generateReq([self.subjectDict["6.041"], self.subjectDict["18.440"]], 1), Requirement([], 1, self.subjectDict["6.003"])], 2))
        term.setReq(self.subjectDict["6.012"], Requirement([], 1, self.subjectDict["6.002"]))
        term.setReq(self.subjectDict["6.013"], Requirement().generateReq([self.subjectDict["6.003"], self.subjectDict["6.007"]], 1))
        term.setReq(self.subjectDict["6.022J"], Requirement().generateReq([self.subjectDict["8.02"], self.subjectDict["18.03"]], 1))
        term.setReq(self.subjectDict["6.033"], Requirement([], 1, self.subjectDict["6.004"]))
        term.setReq(self.subjectDict["6.042"], Requirement([], 1, self.subjectDict["18.01"]))
        term.setReq(self.subjectDict["6.045J"], Requirement([], 1, self.subjectDict["6.042"]))
        term.setReq(self.subjectDict["6.046"], Requirement([], 1, self.subjectDict["6.006"]))
        term.setReq(self.subjectDict["6.061"], Requirement().generateReq([self.subjectDict["6.002"], self.subjectDict["6.013"]], 1))
        term.setReq(self.subjectDict["6.071J"], Requirement([], 1, self.subjectDict["18.03"]))
        term.setReq(self.subjectDict["6.142J"], Requirement([], 1, self.subjectDict["6.141J"]))
        term.setReq(self.subjectDict["6.161"], Requirement([], 1, self.subjectDict["6.003"]))
        term.setReq(self.subjectDict["6.172"], Requirement().generateReq([self.subjectDict["6.004"], self.subjectDict["6.005"], self.subjectDict["6.006"]], 1))
        term.setReq(self.subjectDict["6.173"], Requirement([], 1, self.subjectDict["6.004"]))
        term.setReq(self.subjectDict["6.281J"], Requirement([], 1, self.subjectDict["6.041"]))
        term.setReq(self.subjectDict["6.302"], Requirement().generateReq([self.subjectDict["6.012"], self.subjectDict["2.003"], self.subjectDict["16.04"]], 1))
        term.setReq(self.subjectDict["6.376"], Requirement([], 1, self.subjectDict["6.301"]))
        term.setReq(self.subjectDict["6.443J"], Requirement([], 1, self.subjectDict["18.435"]))
        term.setReq(self.subjectDict["6.452"], Requirement([], 1, self.subjectDict["6.045"]))
        term.setReq(self.subjectDict["6.701"], Requirement([], 1, self.subjectDict["6.003"]))
        term.setReq(self.subjectDict["6.719"], Requirement([], 1, self.subjectDict["6.003"]))
        term.setReq(self.subjectDict["6.774"], Requirement([], 1, self.subjectDict["6.152J"]))
        term.setReq(self.subjectDict["6.775"], Requirement([], 1, self.subjectDict["6.301"]))
        term.setReq(self.subjectDict["6.778J"], Requirement([], 1, self.subjectDict["3.155"]))
        term.setReq(self.subjectDict["6.801"], Requirement([], 1, self.subjectDict["6.003"]))
        term.setReq(self.subjectDict["6.803"], Requirement([], 1, self.subjectDict["6.034"]))
        term.setReq(self.subjectDict["6.820"], Requirement([], 1, self.subjectDict["6.035"]))
        term.setReq(self.subjectDict["6.823"], Requirement([], 1, self.subjectDict["6.004"]))
        term.setReq(self.subjectDict["6.829"], Requirement([], 1, self.subjectDict["6.033"]))
        term.setReq(self.subjectDict["6.833"], Requirement([], 1, self.subjectDict["6.034"]))
        term.setReq(self.subjectDict["6.838"], Requirement([], 1, self.subjectDict["6.837"]))
        term.setReq(self.subjectDict["6.841J"], Requirement([], 1, self.subjectDict["18.404"]))
        term.setReq(self.subjectDict["6.849"], Requirement([], 1, self.subjectDict["6.046"]))
        term.setReq(self.subjectDict["6.850"], Requirement([], 1, self.subjectDict["6.046"]))
        term.setReq(self.subjectDict["6.851"], Requirement([], 1, self.subjectDict["6.046"]))
        term.setReq(self.subjectDict["6.852J"], Requirement([], 1, self.subjectDict["6.046"]))
        term.setReq(self.subjectDict["6.858"], Requirement([], 1, self.subjectDict["6.033"]))
        term.setReq(self.subjectDict["6.872J"], Requirement([], 1, self.subjectDict["6.034"]))
        term.setReq(self.subjectDict["6.876J"], Requirement([], 1, self.subjectDict["6.875"]))
        term.setReq(self.subjectDict["6.922"], Requirement([], 1, self.subjectDict["6.921"]))
        term.setReq(self.subjectDict["6.923"], Requirement([], 1, self.subjectDict["6.922"]))
        term.setReq(self.subjectDict["6.952"], Requirement([], 1, self.subjectDict["6.951"]))
        term.setReq(self.subjectDict["6.070J"], Requirement())
        term.setReq(self.subjectDict["6.07J"], Requirement())
        term.setReq(self.subjectDict["6.141J"], Requirement())
        term.setReq(self.subjectDict["6.152J"], Requirement())
        term.setReq(self.subjectDict["6.182"], Requirement())
        term.setReq(self.subjectDict["6.454"], Requirement())
        term.setReq(self.subjectDict["6.821"], Requirement())
        term.setReq(self.subjectDict["6.891"], Requirement())
        term.setReq(self.subjectDict["6.892"], Requirement())
        term.setReq(self.subjectDict["6.893"], Requirement())
        term.setReq(self.subjectDict["6.894"], Requirement())
        term.setReq(self.subjectDict["6.895"], Requirement())
        term.setReq(self.subjectDict["6.896"], Requirement())
        term.setReq(self.subjectDict["6.897"], Requirement())
        term.setReq(self.subjectDict["6.898"], Requirement())
        term.setReq(self.subjectDict["6.902J"], Requirement())
        term.setReq(self.subjectDict["6.921"], Requirement())
        term.setReq(self.subjectDict["6.975"], Requirement())
        term.setReq(self.subjectDict["6.976"], Requirement())
        term.setReq(self.subjectDict["6.977"], Requirement())
        term.setReq(self.subjectDict["6.978"], Requirement())
        term.setReq(self.subjectDict["6.982J"], Requirement())
        term.setReq(self.subjectDict["6.982J"], Requirement())
        term.setReq(self.subjectDict["2.005"], Requirement())
        term.setReq(self.subjectDict["20.320"], Requirement())
        term.setReq(self.subjectDict["15.064"], Requirement())
        term.setReq(self.subjectDict["2.006"], Requirement([], 1, self.subjectDict["2.005"]))
        term.setReq(self.subjectDict["2.008"], Requirement([], 1, self.subjectDict["2.005"]))
        term.setReq(self.subjectDict["18.05"], Requirement([], 1, self.subjectDict["18.01"]))
        term.setReq(self.subjectDict["6.035"], Requirement([], 1, self.subjectDict["6.005"]))
        term.setReq(self.subjectDict["6.010"], Requirement().generateReq([self.subjectDict["8.02"]], 1))
    # term.setReq(self.subjectDict["6.337J"], Requirement().generateReq([self.subjectDict["18.03"], self.subjectDict["18.034; 18.06"], self.subjectDict["18.700"], self.subjectDict["18.701"]], 1))
    # term.setReq(self.subjectDict["6.338J"], Requirement().generateReq([self.subjectDict["18.06"], self.subjectDict["18.700"], self.subjectDict["18.701"]], 1))
        term.setReq(self.subjectDict["6.815"], Requirement().generateReq([self.subjectDict["18.06"], self.subjectDict["6.003"]], 1))
    # term.setReq(self.subjectDict["6.455J"], Requirement().generateReq([self.subjectDict["2.004 or 6.003; 6.041; 18.075 or 18.085"],], 1))
        term.setReq(self.subjectDict["6.023J"], Requirement().generateReq([self.subjectDict["2.005"], self.subjectDict["6.021J"], self.subjectDict["20.320"]], 1))
        term.setReq(self.subjectDict["6.522J"], Requirement([Requirement().generateReq([self.subjectDict["2.006"], self.subjectDict["6.013"]], 1), Requirement([], 1, self.subjectDict["6.021J"])], 2))
        term.setReq(self.subjectDict["6.780J"], Requirement().generateReq([self.subjectDict["2.008"], self.subjectDict["6.041"], self.subjectDict["6.152J"], self.subjectDict["15.064"]], 1))
    # term.setReq(self.subjectDict["6.024J"], Requirement().generateReq([self.subjectDict["2.370 or 2.772J; 18.03 or 3.016; GIR:BIOL"],], 2))
        term.setReq(self.subjectDict["6.034"], Requirement().generateReq([self.subjectDict["6.001"], self.subjectDict["6.01"]], 1))
        term.setReq(self.subjectDict["6.827"], Requirement().generateReq([self.subjectDict["6.001"], self.subjectDict["6.042"]], 1))
        term.setReq(self.subjectDict["6.131"], Requirement().generateReq([self.subjectDict["6.002"], self.subjectDict["6.003"], self.subjectDict["6.007"]], 1))
    # term.setReq(self.subjectDict["6.717J"], Requirement().generateReq([self.subjectDict["6.003 or 2.004, 8.02;"],], 1))
    # term.setReq(self.subjectDict["6.777J"], Requirement().generateReq([self.subjectDict["6.003 or 2.004, 8.02;"],], 1))
        term.setReq(self.subjectDict["6.241"], Requirement().generateReq([self.subjectDict["6.003"], self.subjectDict["18.06"]], 1))
        term.setReq(self.subjectDict["6.865"], Requirement().generateReq([self.subjectDict["6.003"], self.subjectDict["18.06"]], 1))
        term.setReq(self.subjectDict["6.345J"], Requirement().generateReq([self.subjectDict["6.003"], self.subjectDict["6.041"]], 1))
    # term.setReq(self.subjectDict["6.621"], Requirement().generateReq([self.subjectDict["6.003; 6.007"], self.subjectDict["6.013"], self.subjectDict["8.07 or 6.630"],], 1))
    # term.setReq(self.subjectDict["6.602"], Requirement().generateReq([self.subjectDict["6.003; 6.007"], self.subjectDict["6.013"], self.subjectDict["or 8.07"],], 1))
        term.setReq(self.subjectDict["6.813"], Requirement([], 1, self.subjectDict["6.005"]))
        term.setReq(self.subjectDict["6.831"], Requirement([], 1, self.subjectDict["6.005"]))
        term.setReq(self.subjectDict["6.046J"], Requirement([Requirement([Requirement().generateReq([self.subjectDict["6.042"], self.subjectDict["18.310"]], 1), Requirement([], 1, self.subjectDict["6.001"])]), Requirement([], 1, self.subjectDict["6.006"])], 1))
        term.setReq(self.subjectDict["6.853"], Requirement().generateReq([self.subjectDict["6.006"], self.subjectDict["6.046"]], 1))
        term.setReq(self.subjectDict["6.047"], Requirement().generateReq([self.subjectDict["6.006"], self.subjectDict["6.041"], self.subjectDict["7.014"]], 1))
        term.setReq(self.subjectDict["6.878J"], Requirement().generateReq([self.subjectDict["6.006"], self.subjectDict["6.041"], self.subjectDict["7.014"]], 1))
        term.setReq(self.subjectDict["6.440"], Requirement().generateReq([self.subjectDict["6.006"], self.subjectDict["6.045"]], 1))
    # term.setReq(self.subjectDict["6.720J"], Requirement().generateReq([self.subjectDict["6.012"], self.subjectDict["3.42"],], 1))
    # term.setReq(self.subjectDict["6.608J"], Requirement().generateReq([self.subjectDict["6.013"], self.subjectDict["8.07"],], 1))
    # term.setReq(self.subjectDict["6.561J"], Requirement().generateReq([self.subjectDict["6.013"], self.subjectDict["2.005"], self.subjectDict["10.302"],], 1))
    # term.setReq(self.subjectDict["6.730"], Requirement().generateReq([self.subjectDict["6.013"], self.subjectDict["6.728"],], 1))
    # term.setReq(self.subjectDict["6.581J"], Requirement().generateReq([self.subjectDict["6.021J"], self.subjectDict["6.034"], self.subjectDict["6.046"], self.subjectDict["6.336"], self.subjectDict["7.91"], self.subjectDict["18.417"],], 1))
    # term.setReq(self.subjectDict["6.814"], Requirement().generateReq([self.subjectDict["6.033; 6.046 or 6.006;"],], 1))
    # term.setReq(self.subjectDict["6.830"], Requirement().generateReq([self.subjectDict["6.033; 6.046 or 6.006;"],], 1))
    # term.setReq(self.subjectDict["6.873J"], Requirement().generateReq([self.subjectDict["6.034 or HST.947; programming skills"],], 1))
        term.setReq(self.subjectDict["6.207J"], Requirement().generateReq([self.subjectDict["6.041"], self.subjectDict["14.30"]], 1))
    # term.setReq(self.subjectDict["6.263J"], Requirement().generateReq([self.subjectDict["6.041"], self.subjectDict["18.313"],], 1))
        term.setReq(self.subjectDict["6.267"], Requirement().generateReq([self.subjectDict["6.041"], self.subjectDict["6.042"]], 1))
    # term.setReq(self.subjectDict["6.834J"], Requirement().generateReq([self.subjectDict["6.041"], self.subjectDict["6.042; 16.410"], self.subjectDict["16.413"], self.subjectDict["6.034"], self.subjectDict["or 6.825"],], 1))
        term.setReq(self.subjectDict["6.437"], Requirement().generateReq([self.subjectDict["6.041"], self.subjectDict["6.436"]], 1))
    # term.setReq(self.subjectDict["6.438"], Requirement().generateReq([self.subjectDict["6.041"], self.subjectDict["6.436; 18.06"],], 1))
    # term.setReq(self.subjectDict["6.854J"], Requirement().generateReq([self.subjectDict["6.041"], self.subjectDict["6.042"], self.subjectDict["or 18.440; 6.046"],], 1))
    # term.setReq(self.subjectDict["6.845"], Requirement().generateReq([self.subjectDict["6.045"], self.subjectDict["6.840"], self.subjectDict["18.435"],], 1))
    # term.setReq(self.subjectDict["6.855J"], Requirement().generateReq([self.subjectDict["6.046"], self.subjectDict["15.081"],], 1))
        term.setReq(self.subjectDict["6.837"], Requirement().generateReq([self.subjectDict["18.02"], self.subjectDict["6.005"]], 1))
        term.setReq(self.subjectDict["6.842"], Requirement().generateReq([self.subjectDict["6.046"], self.subjectDict["6.840"]], 1))
    # term.setReq(self.subjectDict["6.243"], Requirement().generateReq([self.subjectDict["6.241"], self.subjectDict["18.100"],], 2))
        term.setReq(self.subjectDict["6.256"], Requirement().generateReq([self.subjectDict["6.251"], self.subjectDict["6.255"]], 1))
    # term.setReq(self.subjectDict["6.456"], Requirement().generateReq([self.subjectDict["6.341; 2.687"], self.subjectDict["or 6.011 and 18.06"],], 1))
    # term.setReq(self.subjectDict["6.266"], Requirement().generateReq([self.subjectDict["6.436"], self.subjectDict["6.262"],], 1))
        term.setReq(self.subjectDict["6.641"], Requirement([], 1, self.subjectDict["6.013"]))
        term.setReq(self.subjectDict["6.731"], Requirement().generateReq([self.subjectDict["6.728"], self.subjectDict["6.012"]], 1))
        term.setReq(self.subjectDict["6.870"], Requirement().generateReq([self.subjectDict["6.801"], self.subjectDict["6.869"]], 1))
        term.setReq(self.subjectDict["6.951"], Requirement().generateReq([self.subjectDict["6.921"], self.subjectDict["6.922"], self.subjectDict["6.923"]], 1))
        term.setReq(self.subjectDict["6.804J"], Requirement().generateReq([self.subjectDict["9.07"], self.subjectDict["18.05"], self.subjectDict["6.041"]], 1))
    # term.setReq(self.subjectDict["6.874J"], Requirement().generateReq([self.subjectDict["GIR:BIOL"], self.subjectDict["18.440 or 6.041"],], 1))
        term.setReq(self.subjectDict["6.122J"], Requirement([Requirement().generateReq([self.subjectDict["7.014"], self.subjectDict["8.02"], self.subjectDict["6.00"], self.subjectDict["18.03"]], 4), Requirement().generateReq([self.subjectDict["2.001"], self.subjectDict["20.310"], self.subjectDict["6.02"]], 1)], 2))
    # term.setReq(self.subjectDict["6.524J"], Requirement().generateReq([self.subjectDict["GIR:BIOL; 2.002"], self.subjectDict["2.006"], self.subjectDict["6.013"], self.subjectDict["10.301"], self.subjectDict["or 10.302"],], 1))
        term.setReq(self.subjectDict["6.938"], Requirement().generateReq([self.subjectDict["18.02"]], 1))
        term.setReq(self.subjectDict["6.050J"], Requirement().generateReq([self.subjectDict["8.01"]], 1))
        term.setReq(self.subjectDict["6.946J"], Requirement().generateReq([self.subjectDict["8.01"], self.subjectDict["18.03"]], 1))
        term.setReq(self.subjectDict["6.163"], Requirement().generateReq([self.subjectDict["8.02"]], 1))
        term.setReq(self.subjectDict["6.UAP"], Requirement([], 1, self.subjectDict["6.UAT"]))
        term.setReq(self.subjectDict["8.02"], Requirement([], 1, self.subjectDict["8.01"]))

    def makeMeetings(self, subj, minuteStart, minuteEnd):
        ''' Returns a meetingset comprising meetings that start and end at the specified times each day
        
        '''
        return Meetingset([Meeting(subj, minuteStart+x*1440, minuteEnd+x*1440) for x in range(5)])
    
    def assignMeetings(self, term):
        for subj in term.subjects.values():
            startTime=randint(7, 17)*60
            #print "adding "+ str(self.makeMeetings(subj, startTime, startTime+50)) +" to "+ str(subj)
            term.subjectMsets[subj] =[self.makeMeetings(subj, startTime, startTime+50)]