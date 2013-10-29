# coding=utf8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout 
from django.http import HttpResponseRedirect

from models import *
from forms import *

def login_view(request):   
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]   
            password = form.cleaned_data["password"]   
            user = authenticate(username=username, password=password) 
            if user is not None and user.is_active:
                login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = LoginForm() 
    return render_to_response('main/login.html',context_instance=RequestContext(request,{'title':'login','form':form}))

def logout_view(request):  
    logout(request)  
    return login_view(request)

def index(request):
    events = Event.objects.filter(kind__in=[0,1,2,4])
    for event in events:
        if event.kind == 0 or event.kind == 4:
            question = event.father
            event.title = question.title
            event.content = question.content
            followers = question.follower.all()
            collectors = question.collector.all()
            event.follower_num = len(followers)
            event.collector_num = len(collectors)
            event.followed = followers.filter(id=request.user.id).exists()
            event.collected = collectors.filter(id=request.user.id).exists()
            event.answer_num = len(question.answer_set.all())
            event.comment_num = len(question.comments.all())
        elif event.kind == 1 or event.kind == 2:
            if event.kind == 1:
                answer = event.father
            elif event.kind == 2:
                answer = event.father.answer
            event.title = answer.question.title
            event.content = answer.content
            goods = answer.evaluation_set.filter(kind=0)
            bads = answer.evaluation_set.filter(kind=1)
            sowhats = answer.evaluation_set.filter(kind=2)
            event.good_num = len(goods)
            event.bad_num = len(bads)
            event.sowhat_num = len(sowhats)
            event.gooded = goods.filter(id=request.user.id).exists()
            event.baded = bads.filter(id=request.user.id).exists()
            event.sowhated = sowhats.filter(id=request.user.id).exists()
            event.comment_num = len(answer.comments.all())
    return render_to_response('main/index.html',context_instance=RequestContext(request,{'title':'index','events':events}))

def show_question(request,question_id):
    return render_to_response('main/show_question.html',context_instance=RequestContext(request,{'title':'show_question'}))