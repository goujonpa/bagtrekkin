from django.conf.urls import patterns, include, url
from django.contrib import admin

from bagtrekkin import views as bt_views
from bagtrekkin.api import LuggagesResource, FlightsResource

v1_api = Api(api_name='v1')
v1_apiregister(LuggagesResource())
v1_apiregister(FlightsResource())

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),

    url(r'^$', bt_views.index, name='bt_index'),

    url(r'login\.html', bt_views.login, name='bt_login'),
    url(r'logout\.html', bt_views.logout, name='bt_logout'),
    url(r'signup\.html', bt_views.signup, name='bt_signup'),
    url(r'profile\.html', bt_views.profile, name='bt_profile'),
    url(r'actions\.html', bt_views.actions, name='bt_actions'),
)
