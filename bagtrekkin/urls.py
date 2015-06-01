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

    url(r'login\.html', auth_views.login, {'template_name': 'login.jade'}, name='bt_login'),
    url(r'logout\.html', auth_views.logout_then_login, name='bt_logout'),
    url(r'signup\.html', bt_views.signup, name='bt_signup'),
    url(r'actions\.html', bt_views.actions, name='bt_actions'),

    # url(r'^fligths/', bt_views.fligths, name='bt_flights'),
    # url(r'^fligths/(?P<airline>.*\w+)/', bt_views.checkin, name='bt_airline'),
)
