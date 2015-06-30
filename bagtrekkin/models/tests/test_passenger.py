from django.test import TestCase

from bagtrekkin.models.passenger import Passenger


class PassengerTestCase(TestCase):
    fixtures = ['passengers']

    def test_passenger_full_name(self):
        '''Passenger should be printed as expected'''
        passenger = Passenger.objects.first()
        self.assertEqual(passenger.full_name, '%s %s' % (passenger.first_name, passenger.last_name))

    def test_passenger_unicode(self):
        '''Passenger should be printed as expected'''
        passenger = Passenger.objects.first()
        self.assertEqual(unicode(passenger), '%s - %s' % (passenger.full_name, passenger.email))
