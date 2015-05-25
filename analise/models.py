# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model): 
    user = models.ForeignKey(User)  
    
class Compagnies(models.Model):
    id_company = models.AutoField(primary_key=True,default=1)
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'compagnies'
        
    def __unicode__(self):  
        return unicode("%s" % self.name)


class Employees(models.Model):
    id_employee = models.AutoField(primary_key=True,default=1)
    cpf = models.CharField(unique=True, max_length=255)
    FUNCTION_CHOICES = (
        ('Mulher do check-in', 'Mulher do check-in'),
    )
    function = models.CharField(max_length=255,choices=FUNCTION_CHOICES)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),('Ativo','Ativo'),('Dispensado','Dispensado'),
    )
    status = models.CharField(max_length=255,choices=STATUS_CHOICES)
    token = models.CharField(max_length=255)
    unity = models.CharField(max_length=255)
    id_company = models.ForeignKey(Compagnies, db_column='id_company')

    class Meta:
        managed = False
        db_table = 'employees'
    def __unicode__(self):  
        return unicode("%s" % self.cpf)


class Etickets(models.Model):
    id_eticket = models.AutoField(primary_key=True)
    ticket_number = models.CharField(unique=True, max_length=255)
    id_passenger = models.ForeignKey('Passengers', db_column='id_passenger')
    summary = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'etickets'

    def __unicode__(self):  
        return unicode("%s -%s" % (self.id_eticket,self.id_passenger))

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

    class Meta:
        managed = False
        db_table = 'flights'
    
    def __unicode__(self):  
        return unicode("%s -%s" % (self.id_flight,self.id_eticket))


class Logs(models.Model):
    id_log = models.IntegerField(primary_key=True)
    horodator = models.DateTimeField()
    id_employee = models.ForeignKey(Employees, db_column='id_employee')
    id_luggage = models.ForeignKey('Luggages', db_column='id_luggage')
    id_flight = models.ForeignKey(Flights, db_column='id_flight')
    localisation = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'logs'


class Luggages(models.Model):
    id_luggage = models.AutoField(primary_key=True)
    material_number = models.CharField(max_length=255,unique=True)
    id_passenger = models.ForeignKey('Passengers', db_column='id_passenger')

    class Meta:
        managed = False
        db_table = 'luggages'


class Passengers(models.Model):
    id_user = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    pnr = models.CharField(unique=True, max_length=255)
    #password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'passengers'
    def __unicode__(self):  
        return unicode("%s" % self.full_name)
        
'''
Funcao para criar um usuario
'''
def create_user_profile(sender, instance, created, **kwargs):
    profile = UserProfile()
    profile.user = instance
    profile.save()

models.signals.post_save.connect(create_user_profile, sender=User) 