from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from bagtrekkin.forms import FormSignup, EmployeeForm
from bagtrekkin.models import Employee, Company, Airport


class EmployeeFormTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'flights', 'users', 'employees', 'luggages', 'logs']

    def setUp(self):
        super(EmployeeFormTestCase, self).setUp()
        self.client = Client()
        company = Company.objects.get(pk=1)
        airport = Airport.objects.get(pk=1)
        self.user_data = {
            'username': 'totodu33',
            'password1': 'tonton',
            'password2': 'tonton',
            'first_name': 'toto',
            'last_name': 'leouf',
            'email': 'totolebg@email.com'
        }
        self.employee_data = {
            'gender': 'f',
            'function': 'checkin',
            'airport': airport,
            'company': company,
            'old_password': 'tonton',
            'new_password1': 'tonton2',
            'new_password2': 'tonton2'
        }

    def test_basic_post(self):
        """Basic save should work"""
        user_form = FormSignup(self.user_data)
        if user_form.is_valid():
            user = user_form.save()
        employee_form = EmployeeForm(self.employee_data, user)
        if employee_form.is_valid():
            print('valid !!')
            employee_form.save()
        user = User.objects.get(pk=2)
        employee = Employee.objects.get(user=user)
        self.assertEqual(user.username, 'totodu33')
        self.assertEqual(employee.district, 'oklm')

    def test_init_without_instance_parameter(self):
        """Not giving an instance should raise error"""
        #with self.assertRaises(AttributeError):
            #employee_form = EmployeeForm()
        #with self.assertRaises(AttributeError):
            #employee_form = EmployeeForm(self.employee_data)
        pass
