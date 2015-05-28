# -*- encoding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import formsets

from bagtrekkin.models import Employees, Luggages, Flights, Passengers, Etickets, Materials


class FormSignup(UserCreationForm):
    function = forms.ChoiceField(choices=settings.FUNCTION_CHOICES, label="Function")
    status = forms.ChoiceField(choices=settings.STATUS_CHOICES, label="Function")
    cpf = forms.CharField(max_length=11)
    token = forms.CharField(max_length=255)
    district = forms.CharField(max_length=255)
    id_company = forms.ChoiceField(choices=settings.COMPANY_CHOICES, label="Company")
    username = forms.RegexField(
        label='Usuario',
        max_length=255,
        regex=r'^[\w-]+$',
        help_text='Maximo de 255 caracteres. Apenas caracteres alfanumericos (letras, digitos, hifens e underline).',
        error_message='Campo deve conter apenas letras, digitos, hifens e underline com 255 caracteres.'
    )

    class Meta:
        model = User
        # fields=("username","name","cpf","password","function","status","token","district","id_company")
        fields = ("username", "email")
        exclude = ("name", "password")
        widgets = {
            'password': forms.PasswordInput(),
            'set_password': forms.PasswordInput(),
        }


class FormCheckIn(forms.ModelForm):

    class Meta:
        model = Luggages
        exclude = ("id_luggage",)


class FormFligths(forms.ModelForm):

    class Meta:
        model = Flights
        exclude = ("id_flight",)
