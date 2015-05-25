# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
import settings
import os
#from django.views.generic.base import TemplateView

PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

urlpatterns = patterns('',
    #url(r'^$',"analise.views.inicio"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',"analise.views.inicio"),
    url(r"^media/(?P<path>.*)$","django.views.static.serve",{"document_root":settings.MEDIA_ROOT}), 
    url(r'^bagtrekkin/cadastro/$',"analise.views.cadastro"),  
    url(r'^bagtrekkin/login/',"django.contrib.auth.views.login",{"template_name":"login.html"}),
    url(r'^index/$',"analise.views.index"),
    url(r'^bagtrekkin/logout/',"django.contrib.auth.views.logout_then_login",{"login_url":"/bagtrekkin/login/"}),
    url(r'^check-in/$',"analise.views.checkin"), #deprecated **************
    url(r'^fligths/$',"analise.views.fligths"),
    url(r'^fligths/(?P<airline>.*\w+)/$',"analise.views.checkin"),
)
