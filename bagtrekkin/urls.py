# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from bagtrekkin.api import MaterialsResource

materials_resource = MaterialsResource()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(materials_resource.urls)),

    url(r'^$', "bagtrekkin.views.index"),

    url(r'^login/', "django.contrib.auth.views.login", {"template_name": "login.html"}),
    url(r'^logout/', "django.contrib.auth.views.logout_then_login", {"login_url": "/login/"}),

    url(r'^signup/$', "bagtrekkin.views.signup"),

    url(r'^checkin/$', "bagtrekkin.views.checkin"),
    url(r'^fligths/$', "bagtrekkin.views.fligths"),
    url(r'^fligths/(?P<airline>.*\w+)/$', "bagtrekkin.views.checkin"),
)
