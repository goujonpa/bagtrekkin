from django.conf.urls import patterns, include, url
from django.contrib import admin

from bagtrekkin.api.urls import bt_api
from bagtrekkin.views.index import index as bt_index
from bagtrekkin.views.login import login as bt_login
from bagtrekkin.views.logout import logout as bt_logout
from bagtrekkin.views.profile import profile as bt_profile
from bagtrekkin.views.search import search as bt_search
from bagtrekkin.views.signup import signup as bt_signup
from bagtrekkin.views.parallax import parallax as bt_parallax

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(bt_api.urls)),

    url(r'home/^$', bt_index, name='bt_index'),
    url(r'^$', bt_parallax, name='bt_parallax'),
    url(r'^login\.html', bt_login, name='bt_login'),
    url(r'^logout\.html', bt_logout, name='bt_logout'),
    url(r'^signup\.html', bt_signup, name='bt_signup'),
    url(r'^profile\.html', bt_profile, name='bt_profile'),
    url(r'^search\.html', bt_search, name='bt_search'),
)
