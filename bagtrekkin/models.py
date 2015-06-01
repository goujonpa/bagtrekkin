from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponseServerError

from tastypie.models import create_api_key

from bagtrekkin.utils import generate_token

GENDER_CHOICES = (
    ('f', 'F'),
    ('m', 'M'),
)
FUNCTION_CHOICES = (
    ('checkin', 'Check-In'),
    ('ramp', 'Ramp'),
    ('lostfounds', 'Lost and Founds'),
)
STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('blocked', 'Blocked'),
)


class Compagny(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return unicode('%s' % self.name)


class Employee(models.Model):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    token = models.CharField(max_length=254)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, blank=True, null=True)
    function = models.CharField(max_length=32, choices=FUNCTION_CHOICES, blank=True, null=True)
    company = models.ForeignKey(Compagny, blank=True, null=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return unicode('%s <%s>' % (self.user.get_full_name(), self.user.email))

    def save(self, *args, **kwargs):
        '''Generate a new token based on email'''
        if self.pk is not None:
            orig = Employee.objects.get(pk=self.pk)
            if orig.user.email != self.user.email:
                self.token = generate_token(self.user.email)
        else:
            self.token = generate_token(self.user.email)
        super(Employee, self).save(*args, **kwargs)


class Passenger(models.Model):
    email = models.CharField(max_length=254, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    pnr = models.CharField(max_length=6, unique=True)
    tel = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode('%s <%s>' % (self.full_name, self.email))

    @property
    def full_name(self):
        return '%s %s %s' % (self.gender, self.first_name, self.last_name)


class Eticket(models.Model):
    ticket_number = models.CharField(max_length=14, unique=True)
    summary = models.CharField(max_length=64)
    passenger = models.ForeignKey(Passenger)

    def __unicode__(self):
        return unicode('%s <%s>' % (self.passenger, self.eticket))


class Flight(models.Model):
    airline = models.CharField(max_length=6)
    aircraft = models.CharField(max_length=64)
    departure_loc = models.CharField(max_length=254)
    departure_time = models.TimeField()
    arrival_loc = models.CharField(max_length=254)
    arrival_time = models.TimeField()
    flight_date = models.DateField()
    duration = models.TimeField()
    eticket = models.ForeignKey(Eticket)
    company = models.ForeignKey(Compagny)

    def __unicode__(self):
        return unicode('%s <%s - %s>' % (self.eticket, self.airline, self.company))


class Material(models.Model):
    material_number = models.CharField(max_length=16)
    datetime = models.DateTimeField(auto_now_add=True)
    is_already_read = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode('%s <%s>' % (self.material_number, self.datetime.strftime('%d, %b %Y @ %H:%m')))

    def save(self, *args, **kwargs):
        '''Fetch materials since one hour with the given material number'''
        materials = Materials.objects.filter(
            datetime__gte=datetime.now()-timedelta(hours=1),
            material_number=self.material_number
        )
        if not materials:
            super(Material, self).save(*args, **kwargs)

    def get_unreads():
        '''Fetch all unread materials ordered by dateime DESC'''
        return Materials.objects.filter(
            is_already_read=False
        ).order_by('-datetime')


class Luggage(models.Model):
    material = models.ForeignKey(Material)
    passenger = models.ForeignKey(Passenger)

    def __unicode__(self):
        return unicode('%s <%s>' % (self.passenger, self.material))


class Log(models.Model):
    horodator = models.DateTimeField(auto_now_add=True)
    localisation = models.CharField(max_length=254)
    employee = models.ForeignKey(Employee)
    luggage = models.ForeignKey(Luggage)
    flight = models.ForeignKey(Flight)

    def save(self, *args, **kwargs):
        '''Add employee district as default localisation'''
        if not self.localisation:
            self.localisation = self.employee.district
            super(Log, self).save(*args, **kwargs)


def create_employee(sender, instance, created, **kwargs):
    if created:
        employee, _ = Employee.objects.get_or_create(user=instance)
        employee.save()


models.signals.post_save.connect(create_api_key, sender=User)
models.signals.post_save.connect(create_employee, sender=User)
