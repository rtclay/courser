from django.http import HttpResponse 
from django.shortcuts import render_to_response
from courserwebview.models import CWVSubject

def index(request):
    subj_list = CWVSubject.objects.all()[:5]
    return render_to_response('index.html', {'subj_list': subj_list})

def display_subjects(request):
    subj_list = CWVSubject.objects.all()
    return render_to_response('subj_list.html', {'subj_list': subj_list})