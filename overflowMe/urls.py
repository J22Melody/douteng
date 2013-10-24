# coding=utf8

from django.conf.urls import patterns, include, url
from django.conf import settings

from main.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^question/(?P<question_id>\d+)/$', show_question), 
)

# media access
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT, }),
)
