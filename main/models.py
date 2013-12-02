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

class Eventable(models.Model):
    class Meta:
        abstract = True

    events = generic.GenericRelation('Event',content_type_field='content_type',object_id_field='obj_id') 

class Profile(Eventable):
    MAN = 0
    WOMAN = 1
    SEX = ((MAN,'男'),(WOMAN,'女'),)

    portrait = models.ImageField(upload_to="avatar/",default="avatar/DSC_1682.jpg")
    phone = models.CharField(max_length=20,blank=True)
    sex = models.PositiveSmallIntegerField(choices=SEX,blank=True,null=True)
    introduction = models.TextField(blank=True)
    user = models.OneToOneField(User,primary_key=True)
    score = models.IntegerField(default=100)
    follower = models.ManyToManyField(User,related_name="followed")

class Topic(Eventable):
    title = models.CharField(max_length=20)
    description = models.TextField()
    creater = models.ForeignKey(User,related_name="topic_ed")
    follower = models.ManyToManyField(User,related_name="topic_followed",blank=True,null=True)
    father = models.ForeignKey('self',blank=True,null=True)

    def __unicode__(self):
        return self.title


class Question(Commentable,Eventable):
    title = models.CharField(max_length=50)
    content = models.TextField()
    score = models.IntegerField()
    asker = models.ForeignKey(User,related_name="question_asked")
    follower = models.ManyToManyField(User,related_name="question_followed",blank=True,null=True)
    collector = models.ManyToManyField(User,related_name="question_collected",blank=True,null=True)
    topic = models.ManyToManyField(Topic,blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class Answer(Commentable,Eventable):
    content = models.TextField()
    adopted = models.BooleanField(default=False)
    answerer = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
class Evaluation(Eventable):
    GOOD = 0
    BAD = 1
    SOWHAT = 2
    KIND = ((GOOD,'赞同'),(BAD,'反对'),(SOWHAT,"不屑一顾"))

    kind = models.PositiveSmallIntegerField(choices=KIND)
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)

class Comment(Eventable):
    user = models.ForeignKey(User)
    target = models.ForeignKey(User,related_name="comment_to_me",blank=True,null=True)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
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
    # 6：关注（话题） 关注者、话题
    
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
        event = Event(kind=5,user=User.objects.get(id=list(pk_set)[0]),father=instance.user)
        event.save()

@receiver(m2m_changed, sender=Topic.follower.through)
def topic_follower_add(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        event = Event(kind=6,user=User.objects.get(id=list(pk_set)[0]),father=instance)
        event.save()

@receiver(m2m_changed, sender=Question.follower.through)
def question_follower_del(sender, instance, action, pk_set, **kwargs):
    if action == "post_remove":
        event = Event.objects.get(kind=4,user_id=list(pk_set)[0],obj_id=instance.id)
        event.delete()

@receiver(m2m_changed, sender=Profile.follower.through)
def user_follower_del(sender, instance, action, pk_set, **kwargs):
    if action == "post_remove":
        event = Event.objects.get(kind=5,user_id=list(pk_set)[0],obj_id=instance.user.id)
        event.delete()

@receiver(m2m_changed, sender=Topic.follower.through)
def topic_follower_del(sender, instance, action, pk_set, **kwargs):
    if action == "post_remove":
        event = Event.objects.get(kind=6,user_id=list(pk_set)[0],obj_id=instance.id)
        event.save()