from django.db import models

from bagtrekkin.models.eticket import Eticket
from bagtrekkin.models.passenger import Passenger


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
