# Create your views here.
# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
import os
import subprocess
from bagtrekkin.forms import FormCadastro, FormCheckIn, FormFligths
from django.contrib.auth.models import User
from bagtrekkin.models import UserProfile, Passengers, Luggages, Flights
import Bagtrekking.settings
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


def inicio(request):
    return render_to_response("templates/inicio.html",{})

def cadastro(request):
    if request.method=="POST":
        form=FormCadastro(request.POST,request.FILES)
        if form.is_valid():
            item=form.save(commit=False)
            dados=form.cleaned_data
            form.save()
            u=User.objects.get(username=item.username)
            us=UserProfile.objects.get_or_create(user=u)
            us=UserProfile.objects.get(user=u)
            us.save()
            return render_to_response("cadastro_sucesso.html",{})
        else:
            process=subprocess.Popen("python "+str(os.path.join(PROJECT_ROOT_PATH,"rfid_reader.py")),shell=1)
            process.wait()
            form=FormCadastro()
            tag=""
            try:
                tag_file=open("tag.txt")
                tag=tag_file.read()
            except IOError:
                pass
            context={"form":form,"tag":tag}
            context.update(csrf(request))
            return render_to_response("cadastro.html",context)
    else:
        form=FormCadastro()
        context={"form":form}
        context.update(csrf(request))
        return render_to_response("cadastro.html",context)

@login_required
def index(request):
    return render_to_response("index.html")

@login_required
def checkin(request,airline):
    if request.method=="POST":
        form=FormCheckIn(request.POST,request.FILES)
        if form.is_valid():
            item=form.save(commit=False)
            dados=form.cleaned_data
            l=Luggages.objects.filter(id_passenger=item.id_passenger)[0]
            l.id_passenger=dados["id_passenger"]
            l.save()
            form.save()
        else:
            process=subprocess.Popen("python "+str(os.path.join(PROJECT_ROOT_PATH,"rfid_reader.py")),shell=1)
            process.wait()
            form=FormCheckIn()
            tag=""
            try:
                tag_file=open("tag.txt")
                tag=tag_file.read()
            except IOError:
                pass
            context={"form":form,"tag":tag}
            context.update(csrf(request))
            return render_to_response("checkin.html",context)
    else:
        form=FormCheckIn()
        print form
        context={"form":form}
        context.update(csrf(request))
        return render_to_response("checkin.html",context)

@login_required
def fligths(request):
    all_fligths=Flights.objects.filter().values("airline").distinct()
    print all_fligths
    context={"fligths":all_fligths}
    context.update(csrf(request))
    return render_to_response("fligths.html",context)

