from django.contrib.auth.models import User
from django.test import TestCase

from bagtrekkin.models import Employee


class SignupViewTestCase(TestCase):

    def test_signup_get(self):
        with self.assertTemplateUsed('signup.jade'):
            response = self.client.get('/signup.html')
            self.assertEqual(response.status_code, 200)

    def test_signup_post_invalid_no_field(self):
        with self.assertTemplateUsed('signup.jade'):
            response = self.client.post('/signup.html', {})
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'first_name', 'This field is required.')
            self.assertFormError(response, 'form', 'last_name', 'This field is required.')
            self.assertFormError(response, 'form', 'username', 'This field is required.')
            self.assertFormError(response, 'form', 'email', 'This field is required.')
            self.assertFormError(response, 'form', 'password1', 'This field is required.')
            self.assertFormError(response, 'form', 'password2', 'This field is required.')

    def test_signup_post_successful(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Employee.objects.count(), 0)
        response = self.client.post('/signup.html', {
            'username': 'jeanvaljean',
            'first_name': 'Jean',
            'last_name': 'Valjean',
            'email': 'jeanvaljean@space.com',
            'password1': '123',
            'password2': '123'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertRedirects(response, 'http://testserver/search.html')
        self.assertIn('_auth_user_id', self.client.session)
