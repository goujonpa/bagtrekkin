from django.test import TestCase
from django.test import Client

from bagtrekkin.models import Log


class LogTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'flights', 'users', 'employees', 'luggages', 'logs']

    def test_log_unicode(self):
        """Log should be printed as expected"""
        log = Log.objects.first()
        self.assertEqual(unicode(log), '%s (%s) - %s - %s' % (
            log.airport, log.stage, log.luggage, log.datetime.strftime('%d, %b %Y @ %H:%m')
        ))
