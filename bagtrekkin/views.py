from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from bagtrekkin.forms import FormSignup, EmployeeForm, SearchForm, CheckinForm, CurrentFlightForm


def index(request):
    return render(request, 'index.jade')


def signup(request):
    if request.method == 'POST':
        form = FormSignup(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            auth_login(request, user)
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
        import ipdb
        ipdb.set_trace()
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            context = {'search_result': search_form.search()}
    else:
        context = {}
        search_form = SearchForm()
        context['search_form'] = search_form
        if not request.session.get('current_flight', False):
            current_flight_form = CurrentFlightForm(request.user)
            context['current_flight_form'] = current_flight_form
        else:
            checkin_form = CheckinForm()
            context['checkin_form'] = checkin_form
        context.update(csrf(request))
        return render(request, 'actions.jade', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bt_actions'))
        else:
            context = {'form': form}
            context.update(csrf(request))
            return render(request, 'profile.jade', context)
    else:
        form = EmployeeForm(instance=request.user)
        context = {'form': form}
        context.update(csrf(request))
        return render(request, 'profile.jade', context)


def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('bt_actions'))
        else:
            context = {'form': form}
            context.update(csrf(request))
            return render(request, 'login.jade', context)
    else:
        form = AuthenticationForm()
        context = {'form': form}
        context.update(csrf(request))
        return render(request, 'login.jade', context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('bt_index'))
