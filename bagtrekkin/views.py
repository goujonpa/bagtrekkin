from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from bagtrekkin.forms import FormSignup, EmployeeForm, SearchForm
from bagtrekkin.models import Luggage, Passenger, Log


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
            return HttpResponseRedirect(reverse('bt_search'))
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
def search(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        context = {
            'search_form': search_form
        }
        try:
            if search_form.is_valid():
                passenger, luggages, logs = search_form.search()
                context.update({
                    'passenger': passenger,
                    'luggages': luggages,
                    'logs': logs
                    })
        except Luggage.DoesNotExist:
            context.update({'error_message': 'Luggage not found'})
        except Log.DoesNotExist:
            context.update({'error_message': 'Logs not found'})
        except Passenger.DoesNotExist:
            context.update({'error_message': 'Passenger not found'})
        return render(request, 'search.jade', context)
    else:
        context = {
            'search_form': SearchForm(),
        }
        context.update(csrf(request))
        return render(request, 'search.jade', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bt_search'))
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
                return HttpResponseRedirect(reverse('bt_search'))
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
    auth_logout(request)
    return HttpResponseRedirect(reverse('bt_index'))
