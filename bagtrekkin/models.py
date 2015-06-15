import requests
from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import IntegrityError, models
from django.http import HttpResponseBadRequest
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
        return '%s %s' % (self.first_name, self.last_name)


class Flight(models.Model):
    airline = models.CharField(max_length=10)
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
    def list_potentials(user):
        '''Fetch all potentials flights regarding user company'''
        return Flight.objects.filter(
            company=user.employee.company
        ).order_by('airline')

    @staticmethod
    def get_from_airline(airline):
        '''Retrieve the best Flight object from airline'''
        if airline:
            return Flight.objects.filter(airline__icontains=airline).first()
        else:
            raise Flight.DoesNotExist

    @staticmethod
    def get_from_json(json):
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
            company=Company.objects.filter(name__icontains=company_name).first()
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
    current_flight = models.ForeignKey(Flight, blank=True, null=True, on_delete=models.SET_NULL)
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
    material_number = models.CharField(max_length=30)
    datetime = models.DateTimeField(auto_now_add=True)
    is_already_read = models.BooleanField(default=False)
    passenger = models.ForeignKey(Passenger)

    def __unicode__(self):
        return unicode('%s - %s' % (self.material_number, self.datetime.strftime('%d, %b %Y @ %H:%m')))

    def save(self, *args, **kwargs):
        '''Fetch materials since one hour with the given material number and datetime default'''
        luggages = Luggage.objects.filter(
            datetime__gte=timezone.now()-timedelta(minutes=10),
            material_number=self.material_number
        )
        if not self.datetime:
            self.datetime = timezone.now()
        if not luggages:
            super(Luggage, self).save(*args, **kwargs)

    @staticmethod
    def list_unreads():
        '''Fetch all unread luggages ordered by datetime DESC'''
        return Luggage.objects.filter(
            is_already_read=False
        ).order_by('-datetime')

    @staticmethod
    def filter_from_flight(object_list, flight):
        return object_list.filter(
            passenger__in=Eticket.objects.filter(
                flights=flight
            ).values_list('passenger__pk', flat=True)
        )


class Log(models.Model):
    horodator = models.DateTimeField(auto_now_add=True)
    localisation = models.CharField(max_length=254)
    employee = models.ForeignKey(Employee)
    luggage = models.ForeignKey(Luggage)
    flight = models.ForeignKey(Flight)

    def __unicode__(self):
        return unicode('%s - %s' % (self.localisation, self.luggage))

    def save(self, *args, **kwargs):
        '''Add employee district as default localisation and other defaults'''
        if not self.horodator:
            self.horodator = timezone.now()
        if not self.localisation:
            self.localisation = self.employee.district
        if not self.flight:
            self.flight = self.employee.current_flight
        super(Log, self).save(*args, **kwargs)


def create_employee(sender, instance, created, **kwargs):
    if created:
        employee, _ = Employee.objects.get_or_create(user=instance)
        employee.save()


def build_from_pnr_lastname_material_number(pnr, last_name, material_number):
    try:
        passenger = Passenger.objects.get(pnr=pnr)
        etickets = passenger.eticket_set.all()
    except Passenger.DoesNotExist:
        headers = {'content-type': 'application/json'}
        url = 'http://alfredpnr.favrodd.com/find/%s/%s' % (pnr, last_name)
        response = requests.get(url, headers=headers)
        if response.status_code == requests.codes.ok:
            result = response.json()
            if result.get('status') and result.get('status') == 'success':
                full_name = result['passenger']['fullname']
                if 'mr' in full_name or 'Mr' in full_name:
                    gender = GENDER_CHOICES[1][0]
                else:
                    gender = GENDER_CHOICES[0][0]
                first_name = ' '.join(full_name.split(' ')[:-1])
                last_name = full_name.split(' ')[-1]
                passenger = Passenger(
                    email=result['passenger']['email'],
                    tel=result['passenger']['tel'],
                    first_name=first_name,
                    last_name=last_name,
                    pnr=pnr,
                    gender=gender
                )
                passenger.save()
                etickets = []
                for json_eticket in result['etickets']:
                    number = json_eticket['number']
                    summary = json_eticket['summary']
                    eticket = Eticket(
                        ticket_number=number,
                        summary=summary,
                        passenger=passenger,
                    )
                    try:
                        eticket.save()
                    except IntegrityError:
                        eticket = Eticket.objects.get(ticket_number=number)
                    etickets.append(eticket)
                    for json_flight in result['flights'][number]:
                        eticket.flights.add(Flight.get_from_json(json_flight))
            else:
                raise HttpResponseBadRequest(result)
        else:
            response.raise_for_status()
    finally:
        luggage = Luggage(
            material_number=material_number,
            passenger=passenger,
            is_already_read=True
        )
        luggage.save()
        return passenger, etickets, luggage


models.signals.post_save.connect(create_api_key, sender=User)
models.signals.post_save.connect(create_employee, sender=User)
