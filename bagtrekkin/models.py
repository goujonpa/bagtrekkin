# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User)

    class Meta:
        managed = True
        db_table = 'user_profile'


class Compagnies(models.Model):
    id_company = models.AutoField(primary_key=True, default=1)
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'compagnies'

    def __unicode__(self):
        return unicode("%s" % self.name)


class Employees(models.Model):
    id_employee = models.AutoField(primary_key=True, default=1)
    cpf = models.CharField(unique=True, max_length=255)
    function = models.CharField(max_length=255, choices=settings.FUNCTION_CHOICES)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=settings.STATUS_CHOICES)
    token = models.CharField(max_length=255, default=None, null=True)
    district = models.CharField(max_length=255)
    id_company = models.ForeignKey(Compagnies, db_column='id_company')

    class Meta:
        managed = True
        db_table = 'employees'

    def __unicode__(self):
        return unicode("%s" % self.cpf)


class Passengers(models.Model):
    id_user = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    pnr = models.CharField(unique=True, max_length=255)
    tel = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'passengers'

    def __unicode__(self):
        return unicode("%s" % self.full_name)


class Etickets(models.Model):
    id_eticket = models.AutoField(primary_key=True)
    ticket_number = models.CharField(unique=True, max_length=255)
    id_passenger = models.ForeignKey(Passengers, db_column='id_passenger')
    summary = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'etickets'

    def __unicode__(self):
        return unicode("%s -%s" % (self.id_eticket, self.id_passenger))


class Flights(models.Model):
    id_flight = models.AutoField(primary_key=True)
    id_eticket = models.ForeignKey(Etickets, db_column='id_eticket')
    aircraft = models.CharField(max_length=255)
    airline = models.CharField(max_length=255)
    departure_loc = models.CharField(max_length=255)
    departure_time = models.TimeField()
    arrival_loc = models.CharField(max_length=255)
    arrival_time = models.TimeField()
    id_company = models.ForeignKey(Compagnies, db_column='id_company')
    flight_date = models.DateField()
    duration = models.TimeField()

    class Meta:
        managed = True
        db_table = 'flights'

    def __unicode__(self):
        return unicode("%s -%s" % (self.id_flight, self.id_eticket))


class Luggages(models.Model):
    id_luggage = models.AutoField(primary_key=True)
    material_number = models.CharField(max_length=255, unique=True)
    id_passenger = models.ForeignKey(Passengers, db_column='id_passenger')

    class Meta:
        managed = True
        db_table = 'luggages'


class Logs(models.Model):
    id_log = models.IntegerField(primary_key=True)
    horodator = models.DateTimeField()
    id_employee = models.ForeignKey(Employees, db_column='id_employee')
    id_luggage = models.ForeignKey(Luggages, db_column='id_luggage')
    id_flight = models.ForeignKey(Flights, db_column='id_flight')
    localisation = models.CharField(max_length=255, default=None, null=True)

    class Meta:
        managed = True
        db_table = 'logs'


def create_user_profile(sender, instance, created, **kwargs):
    '''
    Funcao para criar um usuario
    '''
    profile = UserProfile()
    profile.user = instance
    profile.save()

models.signals.post_save.connect(create_user_profile, sender=User)
