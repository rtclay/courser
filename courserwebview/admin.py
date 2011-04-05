
from courserwebview.models import CWVSubject, CWVCatalog, CWVCoursePlan, \
    CWVMeeting, CWVPerson, CWVReqNot, CWVReqPartial, CWVReqTotal, \
    CWVReqSingleSubject, CWVRequirement, CWVSemesterPlan, CWVStudent, CWVTerm, \
    CWVMeetingSet
from django.contrib import admin

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "departmentCode", "course", "label", "inCharge", "subjectLevel", "totalUnits", "unitsLecture", "unitsLab", "unitsPreparation", "gradeType", "description")
    list_display_links = ('name',)
    list_filter = ('course',)
    search_fields = ('name', 'description', 'inCharge')
    
admin.site.register(CWVSubject,SubjectAdmin) 
admin.site.register(CWVCatalog)
admin.site.register(CWVCoursePlan)
admin.site.register(CWVMeeting)
admin.site.register(CWVMeetingSet)
admin.site.register(CWVPerson)
admin.site.register(CWVReqNot)
admin.site.register(CWVReqPartial)
admin.site.register(CWVReqTotal)
admin.site.register(CWVReqSingleSubject)
admin.site.register(CWVRequirement)
admin.site.register(CWVSemesterPlan)
admin.site.register(CWVStudent)
admin.site.register(CWVTerm)
