from django.test import TestCase

from bagtrekkin.models import Flight


class FlightTestCase(TestCase):
    fixtures = ['companies', 'flights']

    def test_flight_unicode(self):
        """Flight should be printed as expected"""
        flight = Flight.objects.first()
        self.assertEqual(unicode(flight), '%s - %s - %s' % (flight.airline, flight.company, flight.flight_date))
