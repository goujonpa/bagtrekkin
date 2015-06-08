from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from bagtrekkin.forms import FormSignup, FormEmployee, FormSearch


def index(request):
    return render(request, 'index.jade')


def signup(request):
    if request.method == 'POST':
        form = FormSignup(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse('bt_actions'))
        else:
            context = {'form': form}
            context.update(csrf(request))
            return render(request, 'signup.jade', context)
    else:
        form = FormSignup()
        context = {'form': form}
        context.update(csrf(request))
        return render(request, 'signup.jade', context)


@login_required
def actions(request):
    if request.method == 'POST':
        form = FormSearch(request.POST)
        if form.is_valid():
            context = {'search_result': form.search()}
    else:
        form = FormSearch()
        context = {'form': form}
        context.update(csrf(request))
        return render(request, 'actions.jade', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = FormEmployee(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bt_actions'))
        else:
            context = {'form': form}
            context.update(csrf(request))
            return render(request, 'profile.jade', context)
    else:
        form = FormEmployee(instance=request.user)
        context = {'form': form}
        context.update(csrf(request))
        return render(request, 'profile.jade', context)


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
