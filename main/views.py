# coding=utf8

from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response('main/index.html',context_instance=RequestContext(request,{'title':'index'}))

def show_question(request,question_id):
    return render_to_response('main/show_question.html',context_instance=RequestContext(request,{'title':'show_question'}))