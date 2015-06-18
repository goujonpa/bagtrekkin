import requests
from datetime import datetime

from django.contrib.auth.models import User
from django.db import IntegrityError, models
from django.http import HttpResponseBadRequest
from django.utils import timezone

from tastypie.exceptions import BadRequest
from tastypie.models import create_api_key


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


class Airport(models.Model):
    name = models.CharField(max_length=63)
    city = models.CharField(max_length=63)
    country = models.CharField(max_length=63)
    code = models.CharField(max_length=3, unique=True)

    def __unicode__(self):
        return unicode('%s (%s) - %s' % (self.name, self.code, self.country))


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
        '''Concatenate first and last name'''
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
    district = models.CharField(max_length=63, blank=True, null=True)
    status = models.CharField(max_length=31, choices=STATUS_CHOICES, blank=True, null=True)
    function = models.CharField(max_length=31, choices=FUNCTION_CHOICES, blank=True, null=True)
    airport = models.ForeignKey(Airport, blank=True, null=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    current_flight = models.ForeignKey(Flight, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return unicode('%s - %s' % (self.user.get_full_name(), self.user.email))


class Eticket(models.Model):
    ticket_number = models.CharField(max_length=14, unique=True)
    summary = models.CharField(max_length=64)
    passenger = models.ForeignKey(Passenger)
    flights = models.ManyToManyField(Flight)

    def __unicode__(self):
        return unicode('%s - %s' % (self.passenger, self.ticket_number))


class Luggage(models.Model):
    material_number = models.CharField(max_length=30, unique=True)
    passenger = models.ForeignKey(Passenger)

    def __unicode__(self):
        return unicode('%s' % (self.material_number))

    @staticmethod
    def filters_from_flight(flight):
        '''Return a filters dict given a flight'''
        return {
            'passenger__in': Eticket.objects.filter(
                flights=flight
            ).values_list('passenger__pk', flat=True)
        }


class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee)
    luggage = models.ForeignKey(Luggage)
    flight = models.ForeignKey(Flight)

    def __unicode__(self):
        return unicode('%s (%s) - %s - %s' % (
            self.airport, self.stage, self.luggage, self.datetime.strftime('%d, %b %Y @ %H:%m')
        ))

    @property
    def airport(self):
        self.employee.airport

    @property
    def district(self):
        self.employee.district

    @property
    def stage(self):
        self.employee.function

    @property
    def passenger(self):
        self.luggage.passenger

    @property
    def pnr(self):
        self.luggae.passenger.pnr

    @staticmethod
    def create(user, luggage, flight=None):
        '''Create a new Log based on user, using luggage and flight if any'''
        if not luggage.pk:
            raise BadRequest('Luggage can\'t be saved... Please try again.')
        try:
            employee = user.employee
        except Employee.DoesNotExist:
            raise BadRequest(
                'Missing Employee Object for current User. '
                'Please create your profile on web the application.'
            )
        if not flight:
            if employee.current_flight:
                flight = employee.current_flight
            else:
                raise BadRequest(
                    'Missing current_flight for current Employee. '
                    'Please set your current_flight first.'
                )
        datetime = timezone.now()
        Log(
            datetime=datetime, localisation=localisation,
            employee=employee, luggage=luggage, flight=flight
        ).save()


def create_employee(sender, instance, created, **kwargs):
    '''Signal to create an employee for every user creation'''
    if created:
        employee, _ = Employee.objects.get_or_create(user=instance)
        employee.save()


def build_from_pnr_lastname_material_number(pnr, last_name, material_number):
    '''Build passenger, etickets list, luggage objects from PNR and Passenger Last Name'''
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
    luggage = Luggage(
        material_number=material_number,
        passenger=passenger
    )
    luggage.save()
    return passenger, etickets, luggage


models.signals.post_save.connect(create_api_key, sender=User)
models.signals.post_save.connect(create_employee, sender=User)
