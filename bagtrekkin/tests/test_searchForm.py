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

    def form_generation(self, pnr=None, material_number=None):
        data = dict()
        if pnr is not None:
            data.update({'pnr': pnr})
        if material_number is not None:
            data.update({'material_number': material_number})
        form = SearchForm(data)
        self.assertTrue(isinstance(form, SearchForm))
        if (pnr and material_number) or (not pnr and not material_number):
            self.assertFalse(form.is_valid())
        else:
            self.assertTrue(form.is_valid())
        return form

    def test_init_no_data(self):
        """Init should be successful and not valid without provided data"""
        form = self.form_generation()

    def test_init_pnr_data(self):
        """Init should be successful and valid with pnr provided data"""
        form = self.form_generation(pnr='YSVI82')
        self.assertEqual(form.cleaned_data['pnr'], 'YSVI82')

    def test_init_rfid_data(self):
        """Init should be successful and valid with rfid provided data"""
        form = self.form_generation(material_number='FFFFFFFF')
        self.assertEqual(form.cleaned_data['material_number'], 'FFFFFFFF')

    def test_init_two_data_not_valid(self):
        """Form with pnr AND material_number shouldn't be valid (but init successful)"""
        form = self.form_generation(pnr='YSVI82', material_number='FFFFFFFF')

    def test_search_good_pnr(self):
        """Found objects should correspond to what we searched"""
        form = self.form_generation(pnr='ABC123')
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
        form = self.form_generation(material_number='E200 3411 B802 0115 1612 6723')
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
        form = self.form_generation(pnr='caca')
        with self.assertRaises(Passenger.DoesNotExist):
            form.search()

    def test_search_bad_rfid(self):
        """Search from rfid not in db should raise an error"""
        form = self.form_generation(material_number='boudin')
        with self.assertRaises(Luggage.DoesNotExist):
            form.search()
