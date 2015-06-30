from django.db import models

from bagtrekkin.models.flight import Flight
from bagtrekkin.models.passenger import Passenger


class Eticket(models.Model):
    ticket_number = models.CharField(max_length=14, unique=True)
    summary = models.CharField(max_length=64)
    passenger = models.ForeignKey(Passenger)
    flights = models.ManyToManyField(Flight)

    def __unicode__(self):
        return unicode('%s - %s' % (self.passenger, self.ticket_number))
