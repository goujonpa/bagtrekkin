# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tastypie.api import Api

from bagtrekkin import views as bt_views
from bagtrekkin.api import MaterialsResource

materials_resource = MaterialsResource()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(materials_resource.urls)),

    url(r'^$', bt_views.index, name='bt_index'),

    url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='bt_login'),
    url(r'^logout/', auth_views.logout_then_login, name='bt_logout'),

    url(r'^loggedin/', bt_views.loggedin, name='bt_loggedin'),
    url(r'^signup/$', bt_views.signup, name='bt_signup'),

    url(r'^fligths/$', bt_views.fligths, name='bt_flights'),
    url(r'^fligths/(?P<airline>.*\w+)/$', bt_views.checkin, name='bt_airline'),
)
