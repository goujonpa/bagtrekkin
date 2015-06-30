from django.core.exceptions import FieldError
from django.db import models
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
        return self.luggae.passenger.pnr

    @staticmethod
    def create(user, luggage, flight=None, status=LOG_STATUSES[2][0]):
        '''Create a new Log based on user, using luggage and flight if any'''
        if not luggage.pk:
            raise InternalError('Luggage can\'t be saved... Please try again.')
        try:
            employee = user.employee
        except Employee.DoesNotExist:
            raise Employee.DoesNotExist(
                'Missing Employee Object for current User. '
                'Please create your profile on web the application.'
            )
        if not flight:
            if employee.current_flight:
                flight = employee.current_flight
            else:
                raise FieldError(
                    'Missing current_flight for current Employee. '
                    'Please set your current_flight first.'
                )
        datetime = timezone.now()
        Log(
            datetime=datetime, employee=employee,
            luggage=luggage, flight=flight, status=status
        ).save()