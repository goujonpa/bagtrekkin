from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from bagtrekkin.forms import FormSignup


def index(request):
    return render(request, 'index.jade')


def signup(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('bt_actions'))
    else:
        form = FormSignup()
        context = {"form": form}
        context.update(csrf(request))
        return render(request, 'signup.jade', context)


@login_required
def employee(request):
    return render(request, 'employee.jade')


# @login_required
# def checkin(request, airline):
#     if request.method == 'POST':
#         return HttpResponseRedirect(reverse('bt_actions'))
#     else:
#         return render(request, 'checkin.jade')


# @login_required
# def fligths(request):
#     fligths = Flights.objects.values('airline').distinct()
#     context = {'fligths': fligths}
#     context.update(csrf(request))
#     return render(request, 'fligths.jade', context)
