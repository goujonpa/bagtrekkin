from django.test import TestCase
from django.test import Client

from bagtrekkin.forms import FormSignup


class FormSignupTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'flights', 'users', 'employees', 'luggages', 'logs']

    def setUp(self):
        super(FormSignupTestCase, self).setUp()
        self.client = Client()
        self.data = {
            'username': 'totodu33',
            'password1': 'tonton',
            'password2': 'tonton',
            'first_name': 'toto',
            'last_name': 'leouf',
            'email': 'totolebg@email.com'
        }
        self.form = FormSignup(data)

    def test_fields_required(self):
        """Every field should be required"""
        self.assertTrue(self.form.fields['username'].required)
        self.assertTrue(self.form.fields['password1'].required)
        self.assertTrue(self.form.fields['password2'].required)
        self.assertTrue(self.form.fields['first_name'].required)
        self.assertTrue(self.form.fields['last_name'].required)
        self.assertTrue(self.form.fields['email'].required)
