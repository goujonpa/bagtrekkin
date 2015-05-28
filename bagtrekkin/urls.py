# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from bagtrekkin.api import MaterialsResource

materials_resource = MaterialsResource()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(materials_resource.urls, 'api', 'bg-api')),

    url(r'^$', 'bagtrekkin.views.index', name='bg-index'),

    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='bg-login'),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login/'}, name='bg-logout'),

    url(r'^signup/$', 'bagtrekkin.views.signup', name='bg-signup'),

    url(r'^checkin/$', 'bagtrekkin.views.checkin', name='bg-checkin'),
    url(r'^fligths/$', 'bagtrekkin.views.fligths', name='bg-flights'),
    url(r'^fligths/(?P<airline>.*\w+)/$', 'bagtrekkin.views.checkin', name='bg-airline'),
)
