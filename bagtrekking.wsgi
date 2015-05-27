"""
WSGI config for Sequenciamento project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import django.core.handlers.wsgi

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, PROJECT_ROOT)
os.environ["DJANGO_SETTINGS_MODULE"] = "Bagtrekking.settings"
application = django.core.handlers.wsgi.WSGIHandler()
