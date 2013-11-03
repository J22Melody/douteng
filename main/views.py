# coding=utf8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout 
from django.http import HttpResponseRedirect,HttpResponse
from django.utils import simplejson as json
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.auth.decorators import login_required  
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from datetime import timedelta

from lib import *
from models import *
from forms import *

def index(request):
    events = Event.objects.filter(kind__in=[0,1,2,4])
    for event in events:
        if event.kind == 0 or event.kind == 4:
            event.question = event.father
            event.content = event.question.content
            followers = event.question.follower.all()
            collectors = event.question.collector.all()
            event.follower_num = len(followers)
            event.collector_num = len(collectors)
            event.followed = followers.filter(id=request.user.id).exists()
            event.collected = collectors.filter(id=request.user.id).exists()
            event.answer_num = len(event.question.answer_set.all())
            event.comments = event.question.comments.all()
            event.father.type = 0
        elif event.kind == 1 or event.kind == 2:
            if event.kind == 1:
                event.answer = event.father
            elif event.kind == 2:
                event.answer = event.father.answer
            event.question = event.answer.question        
            event.content = event.answer.content
            goods = event.answer.evaluation_set.filter(kind=0)
            bads = event.answer.evaluation_set.filter(kind=1)
            sowhats = event.answer.evaluation_set.filter(kind=2)
            event.good_num = len(goods)
            event.bad_num = len(bads)
            event.sowhat_num = len(sowhats)
            try:
                event.gooded = goods.get(user_id=request.user.id).id
            except ObjectDoesNotExist:
                event.gooded = False
            try:
                event.baded = bads.get(user_id=request.user.id).id
            except ObjectDoesNotExist:
                event.baded = False
            try:
                event.sowhated = sowhats.get(user_id=request.user.id).id
            except ObjectDoesNotExist:
                event.sowhated = False
            event.comments = event.answer.comments.all()          
            event.father.type = 1
        event.title = event.question.title
        event.comment_num = len(event.comments)    
    return render_to_response('main/index.html',context_instance=RequestContext(request,{'title':'index','events':events}))

def topic(request):  
    pass

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

@login_required  
def logout_view(request):  
    logout(request)  
    return login_view(request)

def show_question(request,question_id):
    question = Question.objects.get(id=question_id)
    return render_to_response('main/show_question.html',context_instance=RequestContext(request,{'title':'show_question','question':question}))

@transaction.commit_on_success
def new_question(request):  
    pass

@transaction.commit_on_success
def edit_question(request,question_id):  
    pass

@transaction.commit_on_success
def del_question(request,question_id):  
    pass

@ajax_view
@transaction.commit_on_success
def follow_question(request,question_id):  
    question = Question.objects.get(id=question_id)
    user = request.user
    question.follower.add(user)
    return HttpResponse(json.dumps({"success":True,"text":"取消关注","href":"/question/"+question_id+"/unfollow/","num":""}),mimetype="application/json")

@ajax_view
@transaction.commit_on_success
def unfollow_question(request,question_id):  
    question = Question.objects.get(id=question_id)
    user = request.user
    question.follower.remove(user)
    return HttpResponse(json.dumps({"success":True,"text":"关注","href":"/question/"+question_id+"/follow/","num":str(len(question.follower.all()))+"个"}),mimetype="application/json")

@ajax_view
@transaction.commit_on_success
def collect_question(request,question_id):  
    question = Question.objects.get(id=question_id)
    user = request.user
    question.collector.add(user)
    return HttpResponse(json.dumps({"success":True,"text":"取消收藏","href":"/question/"+question_id+"/uncollect/","num":""}),mimetype="application/json")

@ajax_view
@transaction.commit_on_success
def uncollect_question(request,question_id):  
    question = Question.objects.get(id=question_id)
    user = request.user
    question.collector.remove(user)
    return HttpResponse(json.dumps({"success":True,"text":"收藏","href":"/question/"+question_id+"/collect/","num":str(len(question.collector.all()))+"个"}),mimetype="application/json")

def show_people(request):  
    pass

@transaction.commit_on_success
def new_people(request):  
    pass

@transaction.commit_on_success
def edit_people(request):  
    pass

@transaction.commit_on_success
def del_people(request):  
    pass

@transaction.commit_on_success
def follow_people(request):  
    pass

@transaction.commit_on_success
def unfollow_people(request):  
    pass

def show_topic(request):  
    pass

@transaction.commit_on_success
def new_topic(request):  
    pass

@transaction.commit_on_success
def edit_topic(request):  
    pass

@transaction.commit_on_success
def del_topic(request):  
    pass

@transaction.commit_on_success
def follow_topic(request):  
    pass

@transaction.commit_on_success
def unfollow_topic(request):  
    pass

@ajax_view
@transaction.commit_on_success
def new_eva(request,answer_id,eva_kind):  
    answer = Answer.objects.get(id=answer_id)
    user = request.user
    eva = Evaluation(answer=answer,user=user,kind=eva_kind)
    eva.save()
    kind_des = Evaluation.KIND[int(eva_kind)][1]
    return HttpResponse(json.dumps({"success":True,"text":"取消"+kind_des,"href":"/answer/"+answer_id+"/eva/"+str(eva.id)+"/del/","num":""}),mimetype="application/json")

@ajax_view
@transaction.commit_on_success
def del_eva(request,answer_id,eva_id):  
    answer = Answer.objects.get(id=answer_id)
    eva = Evaluation.objects.get(id=eva_id)
    eva_kind = eva.kind
    kind_des = Evaluation.KIND[eva_kind][1]
    eva.delete()
    num = str(len(answer.evaluation_set.filter(kind=eva_kind)))
    return HttpResponse(json.dumps({"success":True,"text":kind_des,"href":"/answer/"+answer_id+"/eva/"+str(eva_kind)+"/new/","num":num+"个"}),mimetype="application/json")

@ajax_view(method="POST")
@transaction.commit_on_success
def new_comment(request):  
    user = request.user
    content = request.POST.get('content','')
    father = None
    comment = None
    if request.POST.get('father_type') == '0':
        father = Question.objects.get(id=request.POST.get('father_id'))
        father.user = father.asker
    elif request.POST.get('father_type') == '1':
        father = Answer.objects.get(id=request.POST.get('father_id'))
        father.user = father.answerer
    if request.POST.get('target_id',None):
        comment = Comment(user=user,father=father,content=content,target_id=int(request.POST.get('target_id',None)))
    else:
        comment = Comment(user=user,father=father,content=content)
    comment.save()
    comment_id = comment.id
    target_username = ''
    if comment.target:
        target_username = comment.target.username
<<<<<<< HEAD
    create_time = (comment.create_time+timedelta(hours=8)).strftime('%Y年%m月%d日 %H时%M分')
    comment = serializers.serialize('python', [comment,])
    return HttpResponse(json.dumps({"success":True,"create_time":create_time,"comment_id":comment_id,"comment":comment,"target_username":target_username,"username":user.username,"user_id":father.user.id,"father_type":request.POST.get('father_type')},cls=DjangoJSONEncoder),mimetype="application/json")
=======
    comment = serializers.serialize('python', [comment,])
    return HttpResponse(json.dumps({"success":True,"comment_id":comment_id,"comment":comment,"target_username":target_username,"username":user.username,"user_id":father.user.id,"father_type":request.POST.get('father_type')},cls=DjangoJSONEncoder),mimetype="application/json")
>>>>>>> ae6c032274551a59987f6c141b23085d9c3edc19

@ajax_view
@transaction.commit_on_success
def del_comment(request,comment_id):  
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponse(json.dumps({"success":True}),mimetype="application/json")

# def getlist_comment(request,father_type,father_id):
#     if father_type == '0':
#         comments = Question.objects.get(id=father_id).comments.all()
#     elif father_type == '1':
#         comments = Answer.objects.get(id=father_id).comments.all()
#     comments = serializers.serialize('python', comments)
#     return HttpResponse(json.dumps({"success":True,"comments":comments},cls=DjangoJSONEncoder),mimetype="application/json")