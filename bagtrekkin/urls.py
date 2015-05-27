from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "bagtrekkin.views.inicio"),
    url(r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT}),
    url(r'^bagtrekkin/cadastro/$', "bagtrekkin.views.cadastro"),
    url(r'^bagtrekkin/login/', "django.contrib.auth.views.login", {"template_name": "login.html"}),
    url(r'^index/$', "bagtrekkin.views.index"),
    url(r'^bagtrekkin/logout/', "django.contrib.auth.views.logout_then_login", {"login_url": "/bagtrekkin/login/"}),
    url(r'^check-in/$', "bagtrekkin.views.checkin"), #deprecated **************
    url(r'^fligths/$', "bagtrekkin.views.fligths"),
    url(r'^fligths/(?P<airline>.*\w+)/$', "bagtrekkin.views.checkin"),
)
