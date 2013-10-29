# coding=utf8

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver

class Commentable(models.Model):
    class Meta:
        abstract = True

    comments = generic.GenericRelation('Comment',content_type_field='content_type',object_id_field='obj_id')

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
    follower = models.ManyToManyField(User,related_name="followed")

class Topic(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    creater = models.ForeignKey(User,related_name="topic_ed")
    follower = models.ManyToManyField(User,related_name="topic_followed",blank=True,null=True)
    father = models.ForeignKey('self',blank=True,null=True)

class Question(Commentable):
    title = models.CharField(max_length=50)
    content = models.TextField()
    score = models.IntegerField()
    asker = models.ForeignKey(User,related_name="question_asked")
    follower = models.ManyToManyField(User,related_name="question_followed",blank=True,null=True)
    collector = models.ManyToManyField(User,related_name="question_collected",blank=True,null=True)
    topic = models.ManyToManyField(Topic,blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class Answer(Commentable):
    content = models.TextField()
    score = models.IntegerField(default=0)
    answerer = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
class Evaluation(models.Model):
    GOOD = 0
    BAD = 1
    SOWHAT = 2
    KIND = ((GOOD,'赞同'),(BAD,'反对'),(SOWHAT,"dont't give a fuck"))

    kind = models.PositiveSmallIntegerField(choices=KIND)
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)

class Comment(Commentable):
    user = models.ForeignKey(User)
    content = models.TextField()
    create_time = models.DateTimeField()
    content_type = models.ForeignKey(ContentType)
    obj_id = models.PositiveIntegerField()
    father = generic.GenericForeignKey('content_type','obj_id')

class Event(models.Model):  
    kind = models.PositiveSmallIntegerField()
    # 0: 提问 提问者、问题
    # 1：回答 回答者、答案
    # 2：评价 评价者、评价
    # 3：评论 评论者、评论
    # 4：关注（问题）关注者、问题
    # 5：关注（人）关注者、被关注者
    
    user = models.ForeignKey(User)  
    content_type = models.ForeignKey(ContentType)  
    obj_id = models.PositiveIntegerField()   
    father = generic.GenericForeignKey('content_type','obj_id')     
    create_time = models.DateTimeField(auto_now_add=True)  


@receiver(post_save, sender=Question)
def question_post_save(sender, instance, created, **kwargs):
    if created:
        event = Event(kind=0,user=instance.asker,father=instance)
        event.save()

@receiver(post_save, sender=Answer)
def answer_post_save(sender, instance, created, **kwargs):
    if created:
        event = Event(kind=1,user=instance.answerer,father=instance)
        event.save()

@receiver(post_save, sender=Evaluation)
def evaluation_post_save(sender, instance, created, **kwargs):
    if created:
        event = Event(kind=2,user=instance.user,father=instance)
        event.save()

@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    if created:
        event = Event(kind=3,user=instance.user,father=instance)
        event.save()

@receiver(m2m_changed, sender=Question.follower.through)
def question_follower_add(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        event = Event(kind=4,user=User.objects.get(id=list(pk_set)[0]),father=instance)
        event.save()

@receiver(m2m_changed, sender=Profile.follower.through)
def user_follower_add(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        event = Event(kind=5,user=User.objects.get(id=list(pk_set)[0]),father=instance)
        event.save()