from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponseServerError
from django.utils import timezone

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


class Company(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = "companies"

    def __unicode__(self):
        return unicode('%s - %s' % (self.name, self.code))


class Passenger(models.Model):
    email = models.CharField(max_length=254, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    pnr = models.CharField(max_length=6, unique=True)
    tel = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode('%s - %s' % (self.full_name, self.email))

    @property
    def full_name(self):
        return '%s %s %s' % (self.gender, self.first_name, self.last_name)


class Flight(models.Model):
    airline = models.CharField(max_length=6)
    aircraft = models.CharField(max_length=64)
    departure_loc = models.CharField(max_length=254)
    departure_time = models.TimeField()
    arrival_loc = models.CharField(max_length=254)
    arrival_time = models.TimeField()
    flight_date = models.DateField()
    duration = models.DurationField()
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return unicode('%s - %s - %s' % (self.airline, self.company, self.flight_date))

    @staticmethod
    def potentials(user):
        '''Fetch all potentials flights regarding user company'''
        return Flight.objects.filter(
            company=user.employee.company
        ).order_by('airline')

    @staticmethod
    def from_json(json):
        '''Create a new Flight instance given a json'''
        airline = json['airline'].split(' ')[-1]
        company_name = ' '.join(json['airline'].split(' ')[:-1])
        flight_datetime = datetime.strptime(json['date'], "%A, %B %d, %Y")
        flight = Flight(
            airline=airline,
            aircraft=json['aircraft'],
            departure_loc=json['departure']['location'],
            departure_time='%s:00' % json['departure']['time'],
            arrival_loc=json['arrival']['location'],
            arrival_time='%s:00' % json['arrival']['time'],
            flight_date=flight_datetime.date(),
            duration='%s:00' % json['duration'],
            company=Company.objects.filter(name__contains=company_name).first()
        )
        flight.save()
        return flight


class Employee(models.Model):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    token = models.CharField(max_length=254)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, blank=True, null=True)
    function = models.CharField(max_length=32, choices=FUNCTION_CHOICES, blank=True, null=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    current_flight = models.ForeignKey(Flight, blank=True, null=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return unicode('%s - %s' % (self.user.get_full_name(), self.user.email))

    def save(self, *args, **kwargs):
        '''Generate a new token based on email'''
        if self.pk is not None:
            orig = Employee.objects.get(pk=self.pk)
            if orig.user.email != self.user.email:
                self.token = generate_token(self.user.email)
        else:
            self.token = generate_token(self.user.email)
        super(Employee, self).save(*args, **kwargs)


class Eticket(models.Model):
    ticket_number = models.CharField(max_length=14, unique=True)
    summary = models.CharField(max_length=64)
    passenger = models.ForeignKey(Passenger)
    flights = models.ManyToManyField(Flight)

    def __unicode__(self):
        return unicode('%s - %s' % (self.passenger, self.ticket_number))


class Luggage(models.Model):
    material_number = models.CharField(max_length=16)
    datetime = models.DateTimeField(auto_now_add=True)
    is_already_read = models.BooleanField(default=False)
    passenger = models.ForeignKey(Passenger, null=True)

    def __unicode__(self):
        if self.datetime:
            return unicode('%s - %s' % (self.material_number, self.datetime.strftime('%d, %b %Y @ %H:%m')))
        else:
            return unicode('%s' % (self.material_number))

    def save(self, *args, **kwargs):
        '''Fetch materials since one hour with the given material number'''
        luggages = Luggage.objects.filter(
            datetime__gte=timezone.now()-timedelta(minutes=10),
            material_number=self.material_number
        )
        if not luggages:
            super(Luggage, self).save(*args, **kwargs)

    @staticmethod
    def unreads():
        '''Fetch all unread luggages ordered by dateime DESC'''
        return Luggage.objects.filter(
            is_already_read=False
        ).order_by('-datetime')


class Log(models.Model):
    horodator = models.DateTimeField(auto_now_add=True)
    localisation = models.CharField(max_length=254)
    employee = models.ForeignKey(Employee)
    luggage = models.ForeignKey(Luggage)
    flight = models.ForeignKey(Flight)

    def __unicode__(self):
        return unicode('%s - %s' % (self.localisation, self.luggage))

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
