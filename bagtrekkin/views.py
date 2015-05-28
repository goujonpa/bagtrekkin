# -*- encoding: utf-8 -*-
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404

from bagtrekkin.forms import FormSignup, FormCheckIn, FormFligths
from bagtrekkin.models import UserProfile, Passengers, Luggages, Flights
# from bagtrekkin.rfid_reader import readtag


def index(request):
    return render_to_response("index.html", {})


def signup(request):
    if request.method == "POST":
        form = FormSignup(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            data = form.cleaned_data
            form.save()
            u = User.objects.get(username=item.username)
            us = UserProfile.objects.get_or_create(user=u)
            us = UserProfile.objects.get(user=u)
            us.save()
            return render_to_response("signup_successful.html", {})
        else:
            form = FormSignup()
            context = {"form": form}
            context.update(csrf(request))
            return render_to_response("signup.html", context)
    else:
        form = FormSignup()
        context = {"form": form}
        context.update(csrf(request))
        return render_to_response("signup.html", context)


@login_required
def loggedin(request):
    return render_to_response("loggedin.html")


@login_required
def checkin(request, airline):
    if request.method == "POST":
        form = FormCheckIn(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False).cleaned_data
            Luggages(id_passenger=item.id_passenger, id_material=item.id_material).save()
            l.save()
            form.save()
        else:
            form = FormCheckIn()
            context = {"form": form, 'airline': airline}
            context.update(csrf(request))
            return render_to_response("checkin.html", context)
    else:
        form = FormCheckIn()
        context = {"form": form, 'airline': airline}
        context.update(csrf(request))
        return render_to_response("checkin.html", context)


@login_required
def fligths(request):
    all_fligths = Flights.objects.filter().values("airline").distinct()
    context = {"fligths": all_fligths}
    context.update(csrf(request))
    return render_to_response("fligths.html", context)
