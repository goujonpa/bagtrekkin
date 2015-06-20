from django.conf.urls import patterns, include, url
from django.contrib import admin

from bagtrekkin import views as bt_views
from bagtrekkin.api.urls import bt_api

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(bt_api.urls)),

    url(r'^$', bt_views.index, name='bt_index'),

    url(r'login\.html', bt_views.login, name='bt_login'),
    url(r'logout\.html', bt_views.logout, name='bt_logout'),
    url(r'signup\.html', bt_views.signup, name='bt_signup'),
    url(r'profile\.html', bt_views.profile, name='bt_profile'),
    url(r'search\.html', bt_views.search, name='bt_search'),
)
