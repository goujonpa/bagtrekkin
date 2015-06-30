from django.core.exceptions import FieldError
from django.db import models, InternalError
from django.utils import timezone

from bagtrekkin.models.constants import LOG_STATUSES
from bagtrekkin.models.employee import Employee
from bagtrekkin.models.flight import Flight
from bagtrekkin.models.luggage import Luggage


class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee)
    luggage = models.ForeignKey(Luggage)
    flight = models.ForeignKey(Flight)
    status = models.CharField(max_length=31, choices=LOG_STATUSES)

    def __unicode__(self):
        return unicode('%s (%s) - %s - %s' % (
            self.airport, self.stage, self.luggage, self.datetime.strftime('%d, %b %Y @ %H:%m')
        ))

    @property
    def airport(self):
        return self.employee.airport

    @property
    def stage(self):
        return self.employee.function

    @property
    def passenger(self):
        return self.luggage.passenger

    @property
    def pnr(self):
        return self.luggage.passenger.pnr

    @staticmethod
    def create(user, luggage, flight=None, status=LOG_STATUSES[2][0]):
        '''Create a new Log based on user, using luggage and flight if any'''
        if not luggage.pk:
            raise InternalError('Luggage can\'t be saved... Please try again.')
        if not flight:
            if not user.employee.current_flight:
                raise FieldError(
                    'Missing current_flight for current Employee. '
                    'Please set your current_flight first.'
                )
            flight = user.employee.current_flight
        datetime = timezone.now()
        Log(
            datetime=datetime, employee=user.employee,
            luggage=luggage, flight=flight, status=status
        ).save()
