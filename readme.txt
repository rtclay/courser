Courser generates automatic solutions to scheduling requirements, such as those found in college course catalogs. Universities would offer it as a service to their student body.


I'm pleased to announce that I now
have a fully functional prototype of this program.  It is mindful of
subject availability each semester, class time conflicts, unit limits,
subject requirements, and the possible change of requirements from
semester to semester. It's written in Python, and I've attempted to wrestle it into a Django website format but have had little luck so far.

I've started with MIT course 6.3 requirements, but it can be easily
generalized to any goal and any catalog.  Right now I'm using a
simplified dataset with several limitations:
I assume that every semester offers the same classes, and that the
meeting times for each class are a consecutive 50 minute block
(randomly assigned at creation) between the hours of 0800 and 1700,
five days a week.
I have so far ignored GIR and HASS classes.
I've created the dataset with a mixture of manual input and text
editing macros, so it's possible there are some errors in
requirements.
No robust user interface exists, either command line or GUI.



Running these commands will print out a solution to the 6.3 requirements.

from courser.Catalog import Catalog
from courser.CoursePlan import CoursePlan
from courser.Subject import Subject
from courserTests.Dataset import Dataset


dset = Dataset()
dset.dataSetup()
catalog = Catalog(dict(zip([str(x) for x in dset.terms], dset.terms)))
cplan = CoursePlan([], catalog)
goalReq = dset.reqs63
startTerm = dset.terms[0]

cplan.desired = cplan.solveReq(goalReq, startTerm).getSubjects()
cplan.plotRemainingSemesters()

cplan