from mock import patch, MagicMock
from django.test import TestCase

from bagtrekkin.forms import SearchForm
from bagtrekkin.models import Passenger, Luggage, Log

class searchViewTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'etickets', 'flights', 'employees', 'users', 'luggages', 'logs']

    def test_search_redirects(self):
        response = self.client.get('/search.html')
        self.assertRedirects(response, 'http://testserver/login.html?next=/search.html')

    def test_search_logged(self):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('search.jade'):
            response = self.client.get('/search.html')
            self.assertEqual(response.status_code, 200)

    def test_search_post_pnr(self):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('search.jade'):
            response = self.client.post('/search.html', {'pnr': 'ABC123'})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'ABC123')

    def test_search_post_material_number(self):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('search.jade'):
            response = self.client.post('/search.html', {'material_number': 'E200 3411 B802 0115 1612 6723'})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'E200 3411 B802 0115 1612 6723')

    def test_search_post_invalid_no_field(self):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('search.jade'):
            response = self.client.post('/search.html', {})
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'search_form', None, 'Please fill one field')

    def test_search_post_invalid_too_many_fields(self):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('search.jade'):
            response = self.client.post(
                '/search.html',
                {'pnr': 'ABC123', 'material_number': 'E200 3411 B802 0115 1612 6723'}
            )
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'search_form', None, 'Please only fill one field')

    @patch('bagtrekkin.views.SearchForm.search', side_effect=Luggage.DoesNotExist)
    @patch('bagtrekkin.views.SearchForm.is_valid', return_value=True)
    def test_search_post_luggage_does_not_exist(self, mock_is_valid, mock_search):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('search.jade'):
            response = self.client.post('/search.html', {})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Luggages not found')

    @patch('bagtrekkin.views.SearchForm.search', side_effect=Log.DoesNotExist)
    @patch('bagtrekkin.views.SearchForm.is_valid', return_value=True)
    def test_search_post_Log_does_not_exist(self, mock_is_valid, mock_search):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('search.jade'):
            response = self.client.post('/search.html', {})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Logs not found')

    @patch('bagtrekkin.views.SearchForm.search', side_effect=Passenger.DoesNotExist)
    @patch('bagtrekkin.views.SearchForm.is_valid', return_value=True)
    def test_search_post_passenger_does_not_exist(self, mock_is_valid, mock_search):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('search.jade'):
            response = self.client.post('/search.html', {})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Passenger not found')
