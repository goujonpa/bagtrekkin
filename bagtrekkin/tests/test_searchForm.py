from django.test import TestCase
from django.test import Client

from bagtrekkin.forms import SearchForm


class SearchFormTestCase(TestCase):
    fixtures = ['passengers', 'luggages', 'logs']

    def setUp(self):
        pass

    def test_init(self):
        # successful init without data
        form = SearchForm()
        self.assertTrue(isinstance(form, SearchForm))

        # successful init with POST data
        form = SearchForm({'pnr': 'YSVI82', 'material_number': 'FFFFFFFF'})
        self.assertTrue(isinstance(form, SearchForm))
        self.assertEqual(form.fields.get['pnr'], 'YSVI82')
        self.assertEqual(form.fields.get['material_number'], 'FFFFFFFF')

    def test_search(self):
        form = SearchForm()
