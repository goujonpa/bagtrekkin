from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from bagtrekkin.forms.signup_form import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
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
        form = SignupForm()
        context = {'form': form}
        context.update(csrf(request))
        return render(request, 'signup.jade', context)
