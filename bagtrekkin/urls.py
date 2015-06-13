from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from bagtrekkin import views as bt_views
from bagtrekkin.api import (
    UserResource, CompanyResource, PassengerResource, FlightResource,
    EmployeeResource, EticketResource, LuggageResource, LogResource
)

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(CompanyResource())
v1_api.register(PassengerResource())
v1_api.register(FlightResource())
v1_api.register(EmployeeResource())
v1_api.register(EticketResource())
v1_api.register(LuggageResource())
v1_api.register(LogResource())

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
