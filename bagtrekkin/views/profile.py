from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from bagtrekkin.forms.profile_form import ProfileForm


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bt_search'))
        else:
            context = {'form': form}
            context.update(csrf(request))
            return render(request, 'profile.jade', context)
    else:
        form = ProfileForm(instance=request.user)
        context = {'form': form}
        context.update(csrf(request))
        return render(request, 'profile.jade', context)
