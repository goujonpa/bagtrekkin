from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from bagtrekkin import views as bt_views
from bagtrekkin.api import MaterialsResource

materials_resource = MaterialsResource()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(materials_resource.urls)),

    url(r'^$', bt_views.index, name='bt_index'),
    url(r'profile\.html', bt_views.profile, name='bt_profile'),
    url(r'actions\.html', bt_views.actions, name='bt_actions'),

    url(r'^fligths/', bt_views.fligths, name='bt_flights'),
    url(r'^fligths/(?P<airline>.*\w+)/', bt_views.checkin, name='bt_airline'),
)
