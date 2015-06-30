from mock import MagicMock

from django.core.exceptions import FieldError
from django.contrib.auth.models import User
from django.db import InternalError
from django.test import TestCase

from bagtrekkin.models.airport import Airport
from bagtrekkin.models.employee import Employee
from bagtrekkin.models.flight import Flight
from bagtrekkin.models.luggage import Luggage
from bagtrekkin.models.log import Log
from bagtrekkin.models.passenger import Passenger


class LogTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'flights', 'users', 'employees', 'luggages', 'logs']

    def test_log_unicode(self):
        '''Log should be printed as expected'''
        log = Log.objects.first()
        self.assertEqual(unicode(log), '%s (%s) - %s - %s' % (
            log.airport, log.stage, log.luggage, log.datetime.strftime('%d, %b %Y @ %H:%m')
        ))

    def test_aiport(self):
        '''Should return employee's airport'''
        log = Log.objects.first()
        airport = Airport.objects.get(code='MVB')
        self.assertEqual(log.airport, airport)

    def test_stage(self):
        '''Should return employee's function'''
        log = Log.objects.first()
        employee = Employee.objects.first()
        self.assertEqual(log.stage, employee.function)

    def test_passenger(self):
        '''Should return luggage's passenger'''
        log = Log.objects.first()
        passenger = Passenger.objects.first()
        self.assertEqual(log.passenger, passenger)

    def test_pnr(self):
        '''Should return luggage's passenger pnr'''
        log = Log.objects.first()
        passenger = Passenger.objects.first()
        self.assertEqual(log.pnr, passenger.pnr)

    def test_create_no_luggage_pk(self):
        '''Should return an InternalError Luggage can\'t be save'''
        user = MagicMock()
        luggage = MagicMock()
        luggage.pk = None
        with self.assertRaises(InternalError):
            Log.create(user, luggage)

    def test_create_employee_without_current_flight(self):
        '''Should return an Employee.DoesNotExist error'''
        user = MagicMock()
        user.employee.current_flight = None
        luggage = MagicMock()
        luggage.pk = True
        with self.assertRaises(FieldError):
            Log.create(user, luggage)

    def test_create_with_employee_current_flight(self):
        '''Should create a new Log entry'''
        self.assertEqual(Log.objects.count(), 2)
        user = User.objects.first()
        user.employee.current_flight = Flight.objects.first()
        user.employee.save()
        luggage = Luggage.objects.first()
        Log.create(user, luggage)
        self.assertEqual(Log.objects.count(), 3)

    def test_create_with_given_flight(self):
        '''Should create a new Log entry'''
        self.assertEqual(Log.objects.count(), 2)
        user = User.objects.first()
        luggage = Luggage.objects.first()
        flight = Flight.objects.first()
        Log.create(user, luggage, flight)
        self.assertEqual(Log.objects.count(), 3)
