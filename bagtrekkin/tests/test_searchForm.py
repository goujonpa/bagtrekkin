from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment

from bagtrekkin.forms import SearchForm
from bagtrekkin.models import Passenger, Luggage, Log


class SearchFormTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'flights', 'users', 'employees', 'luggages', 'logs']

    def setUp(self):
        super(SearchFormTestCase, self).setUp()
        self._passenger = Passenger.objects.get(pk=1)
        self._luggages = Luggage.objects.filter(passenger=self._passenger)
        self._logs = Log.objects.filter(luggage__passenger=self._passenger)
        self.client = Client()
        self.client.login(username='capflam', password='123')

    def test_init_no_data(self):
        """Init should be successful without provided data"""
        form = SearchForm()
        self.assertTrue(isinstance(form, SearchForm))

    def test_init_pnr_data(self):
        """Init should be successful with pnr provided data"""
        form = SearchForm({'pnr': 'YSVI82'})
        self.assertTrue(isinstance(form, SearchForm))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['pnr'], 'YSVI82')

    def test_init_rfid_data(self):
        """Init should be successful with rfid provided data"""
        form = SearchForm({'material_number': 'FFFFFFFF'})
        self.assertTrue(isinstance(form, SearchForm))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['material_number'], 'FFFFFFFF')

    def test_init_no_data_not_valid(self):
        """Form with no data provided shouldn't be valid"""
        form = SearchForm()
        self.assertTrue(isinstance(form, SearchForm))
        self.assertFalse(form.is_valid())

    def test_init_two_data_not_valid(self):
        """Form with pnr AND material_number shouldn't be valid"""
        form = SearchForm({'pnr': 'YSVI82', 'material_number': 'FFFFFFFF'})
        self.assertTrue(isinstance(form, SearchForm))
        self.assertFalse(form.is_valid())

    def test_search_good_pnr(self):
        """Found objects should correspond to what we searched"""
        form = SearchForm({'pnr': 'ABC123'})
        self.assertTrue(isinstance(form, SearchForm))
        self.assertTrue(form.is_valid())
        passenger, luggages, logs = form.search()
        returned_luggages = [l.pk for l in luggages]
        desired_luggages = [l.pk for l in self._luggages]
        returned_logs = [l.pk for l in logs]
        desired_logs = [l.pk for l in self._logs]
        self.assertEqual(passenger, self._passenger)
        self.assertEqual(returned_luggages, desired_luggages)
        self.assertEqual(returned_logs, desired_logs)

    def test_search_good_rfid(self):
        """Found objects should correspond to what we searched"""
        form = SearchForm({'material_number': 'E200 3411 B802 0115 1612 6723'})
        self.assertTrue(isinstance(form, SearchForm))
        self.assertTrue(form.is_valid())
        passenger, luggages, logs = form.search()
        returned_luggages = [l.pk for l in luggages]
        desired_luggages = [l.pk for l in self._luggages]
        returned_logs = [l.pk for l in logs]
        desired_logs = [l.pk for l in self._logs]
        self.assertEqual(passenger, self._passenger)
        self.assertEqual(returned_luggages, desired_luggages)
        self.assertEqual(returned_logs, desired_logs)

    def test_search_bad_pnr(self):
        """Search from pnr not in db should raise an error"""
        response = self.client.post(reverse('bt_search'), {'pnr': 'caca'})
        form = response.context['search_form']
        self.assertTrue(isinstance(form, SearchForm))
        with self.assertRaises(Passenger.DoesNotExist):
            form.search()

    def test_search_bad_rfid(self):
        """Search from rfid not in db should raise an error"""
        response = self.client.post(reverse('bt_search'), {'material_number': 'boudin'})
        form = response.context['search_form']
        self.assertTrue(isinstance(form, SearchForm))
        with self.assertRaises(Luggage.DoesNotExist):
            form.search()
