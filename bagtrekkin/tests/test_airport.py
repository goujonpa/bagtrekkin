from django.test import TestCase
from django.test import Client

from bagtrekkin.models import Airport


class AirportTestCase(TestCase):
    fixtures = ['airports']

    def test_airport_unicode(self):
        """Airport should be printed as expected"""
        airport = Airport.objects.first()
        self.assertEqual(unicode(airport), '%s (%s) - %s' % (airport.name, airport.code, airport.country))
