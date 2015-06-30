from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from bagtrekkin.forms.login_form import LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            form.confirm_login_allowed(user)
            auth_login(request, user)
            return HttpResponseRedirect(reverse('bt_search'))
        else:
            context = {'form': form}
            context.update(csrf(request))
            return render(request, 'login.jade', context)
    else:
        form = LoginForm()
        context = {'form': form}
        context.update(csrf(request))
        return render(request, 'login.jade', context)
