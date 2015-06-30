from datetime import datetime

from django.db import models

from bagtrekkin.models.company import Company


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
