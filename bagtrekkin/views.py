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

from bagtrekkin.forms import (
    FormSignup, EmployeeForm, SearchForm, CheckinForm,
    SetCurrentFlightForm, FlushCurrentFlightForm
)
from bagtrekkin.models import Flight


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
    context = {}
    if request.method == 'POST':
        if request.POST.get('form_type') == 'Search':
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                search_result = search_form.search()
                context.update({
                    'active': 'Search',
                    'current_flight': Flight.from_session(request.session),
                    'checkin_form': CheckinForm(),
                    'search_form': search_form,
                    'passenger': search_result[0],
                    'luggages': search_result[1],
                    'logs': search_result[2],
                    'set_current_flight_form': SetCurrentFlightForm(request.user),
                    'flush_current_flight_form': FlushCurrentFlightForm()
                })
                return render(request, 'actions.jade', context)
        elif request.POST.get('form_type') == 'Checkin':
            checkin_form = CheckinForm(request.POST)
            if checkin_form.is_valid():
                context.update({
                    'current_flight': Flight.from_session(request.session),
                    'search_form': SearchForm(),
                    'checkin_form': checkin_form,
                    'set_current_flight_form': SetCurrentFlightForm(),
                    'flush_current_flight_form': FlushCurrentFlightForm()
                })
                return render(request, 'actions.jade', context)
        elif request.POST.get('form_type') == 'SetCurrentFlight':
            set_current_flight_form = SetCurrentFlightForm(request.user, request.POST)
            if set_current_flight_form.is_valid():
                request.session['current_flight'] = set_current_flight_form.cleaned_data['current_flight'].id
                context.update({
                    'current_flight': Flight.from_session(request.session),
                    'search_form': SearchForm(),
                    'checkin_form': CheckinForm(),
                    'set_current_flight_form': set_current_flight_form,
                    'flush_current_flight_form': FlushCurrentFlightForm()
                })
                return render(request, 'actions.jade', context)
        elif request.POST.get('form_type') == 'FlushCurrentFlight':
            flush_current_flight_form = FlushCurrentFlightForm(request.POST)
            if flush_current_flight_form.is_valid():
                try:
                    del request.session['current_flight']
                except IndexError:
                    pass
                context.update({
                    'current_flight': Flight.from_session(request.session),
                    'search_form': SearchForm(),
                    'checkin_form': CheckinForm(),
                    'set_current_flight_form': SetCurrentFlightForm(request.user),
                    'flush_current_flight_form': flush_current_flight_form
                })
                return render(request, 'actions.jade', context)
    else:
        if not request.session.get('current_flight'):
            set_current_flight_form = SetCurrentFlightForm(request.user)
            context['set_current_flight_form'] = set_current_flight_form
        else:
            checkin_form = CheckinForm()
            context['checkin_form'] = checkin_form
        context.update({
            'current_flight': Flight.from_session(request.session),
            'search_form': SearchForm(),
            'flush_current_flight_form': FlushCurrentFlightForm()
        })
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
