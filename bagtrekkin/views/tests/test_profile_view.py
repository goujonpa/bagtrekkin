from django.contrib.auth.models import User
from django.test import TestCase


class ProfileViewTestCase(TestCase):
    fixtures = ['airports', 'companies', 'users', 'employees']

    def test_profile_get(self):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('profile.jade'):
            response = self.client.get('/profile.html')
            self.assertEqual(response.status_code, 200)

    def test_profile_post_invalid_no_field(self):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('profile.jade'):
            response = self.client.post('/profile.html', {})
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'gender', 'This field is required.')
            self.assertFormError(response, 'form', 'first_name', 'This field is required.')
            self.assertFormError(response, 'form', 'last_name', 'This field is required.')
            self.assertFormError(response, 'form', 'username', 'This field is required.')
            self.assertFormError(response, 'form', 'email', 'This field is required.')
            self.assertFormError(response, 'form', 'function', 'This field is required.')
            self.assertFormError(response, 'form', 'airport', 'This field is required.')
            self.assertFormError(response, 'form', 'company', 'This field is required.')

    def test_profile_post_successful(self):
        self.client.login(username='capflam', password='123')
        response = self.client.post('/profile.html', {
            'gender': 'm',
            'username': 'capflam',
            'first_name': 'Jean',
            'last_name': 'Valjean',
            'email': 'jeanvaljean@space.com',
            'function': 'ramp',
            'airport': '1',
            'company': '1'
        })
        self.assertEqual(User.objects.first().first_name, 'Jean')
        self.assertEqual(User.objects.first().last_name, 'Valjean')
        self.assertRedirects(response, 'http://testserver/search.html')
