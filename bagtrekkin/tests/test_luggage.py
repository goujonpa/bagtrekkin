from django.test import TestCase

from bagtrekkin.models import Luggage


class LuggageTestCase(TestCase):
    fixtures = ['passengers', 'luggages']

    def test_luggage_unicode(self):
        """Luggage should be printed as expected"""
        luggage = Luggage.objects.first()
        self.assertEqual(unicode(luggage), '%s' % (luggage.material_number))
