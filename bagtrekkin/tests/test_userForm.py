from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from bagtrekkin.forms import FormSignup
from bagtrekkin.models import Employee


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
        self.form = FormSignup(self.data)

    def test_fields_required(self):
        """Every field should be required"""
        self.assertTrue(self.form.fields['username'].required)
        self.assertTrue(self.form.fields['password1'].required)
        self.assertTrue(self.form.fields['password2'].required)
        self.assertTrue(self.form.fields['first_name'].required)
        self.assertTrue(self.form.fields['last_name'].required)
        self.assertTrue(self.form.fields['email'].required)

    def test_employee_is_created(self):
        """Saving a form creates user AND employee LINKED to user"""
        if self.form.is_valid():
            self.form.save()
        user = User.objects.get(username='totodu33')
        self.assertTrue((user is not None))
        employee = Employee.objects.get(user=user)
        self.assertTrue((employee is not None))
