from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('bt_index'))
