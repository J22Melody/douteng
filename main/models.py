# coding=utf8

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    MAN = 0
    WOMAN = 1
    SEX = ((MAN,'男'),(WOMAN,'女'),)

    portrait = models.ImageField(upload_to="portrait/",blank=True,null=True)
    phone = models.CharField(max_length=20,blank=True)
    sex = models.PositiveSmallIntegerField(choices=SEX)
    introduction = models.TextField(blank=True)
    user = models.OneToOneField(User,primary_key =True)
    score = models.IntegerField(default=100)

class Tag(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField()
    father = models.ForeignKey('self',blank=True,null=True)

class Question(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    score = models.IntegerField()
    asker = models.ForeignKey(User,related_name="question_asked")
    follower = models.ManyToManyField(User,related_name="question_followed")
    collector = models.ManyToManyField(User,related_name="question_collected")
    tag = models.ManyToManyField(Tag)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

class Answer(models.Model):
    content = models.TextField()
    score = models.IntegerField(default=0)
    answerer = models.ForeignKey(User)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    
class Evaluation(models.Model):
    GOOD = 0
    BAD = 1
    SOWHAT = 2
    KIND = ((GOOD,'赞同'),(BAD,'反对'),(SOWHAT,"dont't give a fuck"))

    kind = models.PositiveSmallIntegerField(choices=KIND)
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)

class Comment(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    create_time = models.DateTimeField()
    father = models.ForeignKey('self',blank=True,null=True)
    answer = models.ForeignKey(Answer,blank=True,null=True)
    question = models.ForeignKey(Question,blank=True,null=True)
