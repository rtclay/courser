from django.contrib import admin
from courserwebview.models import CWVSubject, CWVCatalog

class CWVSubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "departmentCode", "course", "label", "inCharge", "subjectLevel", "totalUnits", "unitsLecture", "unitsLab", "unitsPreparation", "gradeType", "description")
    list_display_links = ('name',)
    list_filter = ('course',)
    search_fields = ('name', 'description', 'inCharge')
    
admin.site.register(CWVSubject,CWVSubjectAdmin) 
admin.site.register(CWVCatalog)