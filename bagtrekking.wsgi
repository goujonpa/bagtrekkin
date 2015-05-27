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
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, PROJECT_ROOT)
os.environ["DJANGO_SETTINGS_MODULE"] = "Bagtrekking.settings"

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

# import sys, os, bottle

# sys.path = ['/var/www/sequenciamento/'] + sys.path
# os.chdir(os.path.dirname(__file__))
# print sys.path
# import Sequenciamento #This loads your application

# application = bottle.default_app()
