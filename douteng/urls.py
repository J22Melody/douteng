# coding=utf8

from django.conf.urls import patterns, include, url
from django.conf import settings

from main.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', index),
    url(r'^topic/$', topic),

    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),

    url(r'^question/(?P<question_id>\d+)/$', show_question), 
    url(r'^question/new/$', new_question), 
    url(r'^question/search/$', search_question), 
    url(r'^question/(?P<question_id>\d+)/edit/$', edit_question), 
    url(r'^question/(?P<question_id>\d+)/del/$', del_question), 
    url(r'^question/(?P<question_id>\d+)/follow/$', follow_question), 
    url(r'^question/(?P<question_id>\d+)/unfollow/$', unfollow_question), 
    url(r'^question/(?P<question_id>\d+)/collect/$', collect_question), 
    url(r'^question/(?P<question_id>\d+)/uncollect/$', uncollect_question), 
    url(r'^question/(?P<question_id>\d+)/answer/$', answer_question), 

    url(r'^people/(?P<people_id>\d+)/$', show_people), 
    url(r'^people/new/$', new_people), 
    url(r'^people/(?P<people_id>\d+)/edit/$', edit_people), 
    url(r'^people/(?P<people_id>\d+)/del/$', del_people), 
    url(r'^people/(?P<people_id>\d+)/follow/$', follow_people), 
    url(r'^people/(?P<people_id>\d+)/unfollow/$', unfollow_people), 

    url(r'^topic/(?P<topic_id>\d+)/$', show_topic), 
    url(r'^topic/new/$', new_topic), 
    url(r'^topic/(?P<topic_id>\d+)/edit/$', edit_topic), 
    url(r'^topic/(?P<topic_id>\d+)/del/$', del_topic), 
    url(r'^topic/(?P<topic_id>\d+)/follow/$', follow_topic), 
    url(r'^topic/(?P<topic_id>\d+)/unfollow/$', unfollow_topic), 

    url(r'^answer/(?P<answer_id>\d+)/eva/(?P<eva_kind>\d+)/new/$', new_eva),
    url(r'^answer/(?P<answer_id>\d+)/eva/(?P<eva_id>\d+)/del/$', del_eva),

    # url(r'^comment/getlist/(?P<father_type>\d+)/(?P<father_id>\d+)/$', getlist_comment),
    url(r'^comment/new/$', new_comment),
    url(r'^comment/(?P<comment_id>\d+)/del/$', del_comment),
)

# media access
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT, }),
)
