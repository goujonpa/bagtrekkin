from django.test import TestCase
from django.test import Client

from bagtrekkin.models import Eticket


class EticketTestCase(TestCase):
    fixtures = ['companies', 'flights', 'passengers', 'etickets']

    def test_eticket_unicode(self):
        """Eticket should be printed as expected"""
        eticket = Eticket.objects.first()
        self.assertEqual(unicode(eticket), '%s - %s' % (eticket.passenger, eticket.ticket_number))
