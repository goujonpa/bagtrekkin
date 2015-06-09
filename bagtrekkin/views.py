import requests

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
from bagtrekkin.models import GENDER_CHOICES, Flight, Passenger, Eticket


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
                context.update({
                    'current_flight': request.user.employee.current_flight,
                    'checkin_form': CheckinForm(),
                    'search_form': search_form,
                    'set_current_flight_form': SetCurrentFlightForm(request.user),
                    'flush_current_flight_form': FlushCurrentFlightForm()
                })
                return render(request, 'actions.jade', context)
        elif request.POST.get('form_type') == 'Checkin':
            checkin_form = CheckinForm(request.POST)
            if checkin_form.is_valid():
                headers = {'content-type': 'application/json'}
                url = 'http://alfredpnr.favrodd.com/find/%s/%s' % (checkin_form.cleaned_data['pnr'],
                                                                   checkin_form.cleaned_data['name'])
                response = requests.get(url, headers=headers)
                if response.status_code == requests.codes.ok:
                    result = response.json()
                    if result.get('status') and result.get('status') == 'success':
                        full_name = result['passenger']['fullname']
                        if 'mr' in full_name or 'Mr' in full_name:
                            gender = GENDER_CHOICES[1][0]
                        first_name = ' '.join(full_name.split(' ')[:-1])
                        last_name = full_name.split(' ')[-1]
                        passenger = Passenger(
                            email=result['passenger']['email'],
                            tel=result['passenger']['tel'],
                            first_name=first_name,
                            last_name=last_name,
                            pnr=checkin_form.cleaned_data['pnr'],
                            gender=gender
                        )
                        passenger.save()
                        for json_eticket in result['etickets']:
                            number = json_eticket['number']
                            summary = json_eticket['summary']
                            eticket = Eticket(
                                ticket_number=number,
                                summary=summary,
                                passenger=passenger,
                            )
                            eticket.save()
                            for json_flight in result['flights'][number]:
                                eticket.flights.add(Flight.from_json(json_flight))
                context.update({
                    'current_flight': request.user.employee.current_flight,
                    'search_form': SearchForm(),
                    'checkin_form': checkin_form,
                    'set_current_flight_form': SetCurrentFlightForm(request.user),
                    'flush_current_flight_form': FlushCurrentFlightForm()
                })
                return render(request, 'actions.jade', context)
        elif request.POST.get('form_type') == 'SetCurrentFlight':
            set_current_flight_form = SetCurrentFlightForm(request.user, request.POST)
            if set_current_flight_form.is_valid():
                request.user.employee.current_flight = set_current_flight_form.cleaned_data['current_flight']
                request.user.employee.save()
                context.update({
                    'current_flight': request.user.employee.current_flight,
                    'search_form': SearchForm(),
                    'checkin_form': CheckinForm(),
                    'set_current_flight_form': set_current_flight_form,
                    'flush_current_flight_form': FlushCurrentFlightForm()
                })
                return render(request, 'actions.jade', context)
        elif request.POST.get('form_type') == 'FlushCurrentFlight':
            flush_current_flight_form = FlushCurrentFlightForm(request.POST)
            if flush_current_flight_form.is_valid():
                request.user.employee.current_flight = None
                request.user.employee.save()
                context.update({
                    'current_flight': request.user.employee.current_flight,
                    'search_form': SearchForm(),
                    'checkin_form': CheckinForm(),
                    'set_current_flight_form': SetCurrentFlightForm(request.user),
                    'flush_current_flight_form': flush_current_flight_form
                })
                return render(request, 'actions.jade', context)
    else:
        if not request.user.employee.current_flight:
            set_current_flight_form = SetCurrentFlightForm(request.user)
            context['set_current_flight_form'] = set_current_flight_form
        else:
            checkin_form = CheckinForm()
            context['checkin_form'] = checkin_form
        context.update({
            'current_flight': request.user.employee.current_flight,
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
            form = AuthenticationForm()
            context = {'form': form}
            context.update(csrf(request))
            return render(request, 'login.jade', context)
    else:
        form = AuthenticationForm()
        context = {'form': form}
        context.update(csrf(request))
        return render(request, 'login.jade', context)


def logout(request):
    request.user.employee.current_flight = None
    request.user.employee.save()
    auth_logout(request)
    return HttpResponseRedirect(reverse('bt_index'))
