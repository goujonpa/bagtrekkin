from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from bagtrekkin.forms import SignupForm, EmployeeForm
from bagtrekkin.models import Employee, Company, Airport
from bagtrekkin.models import EMPLOYEE_GENDERS, EMPLOYEE_FUNCTIONS


class EmployeeFormTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'flights', 'users', 'employees', 'luggages', 'logs']

    def setUp(self):
        super(EmployeeFormTestCase, self).setUp()
        self.employee_data = {
            'username': 'capflam',
            'first_name': 'Capitain',
            'last_name': 'Flamme',
            'gender': 'f',
            'function': 'ramp',
            'airport': '2',
            'company': '2',
            'old_password': '123',
            'new_password1': 'soleil',
            'new_password2': 'soleil'
        }
        self.client.login(username='capflam', password='123')

    def test_basic_post(self):
        """Basic save should work"""
        user = User.objects.first()
        employee_form = EmployeeForm(self.employee_data, instance=user)
        if employee_form.is_valid():
            employee_form.save()
        else:
            print(employee_form.errors)
        employee = Employee.objects.get(user=user)
        self.assertIsInstance(employee, Employee)
        self.assertEqual(user.username, 'capflam')
        self.assertTrue(user.check_password('soleil'))
        self.assertEqual(employee.airport.code, 'CQF')
        self.assertEqual(employee.company.code, 'RBU')
        self.assertEqual(employee.gender, 'f')
        self.assertEqual(employee.function, 'ramp')

    def test_init_without_instance_parameter(self):
        """Not passing an instance should raise an error"""
        with self.assertRaises(AttributeError):
            employee_form = EmployeeForm()
        with self.assertRaises(AttributeError):
            employee_form = EmployeeForm(self.employee_data)

    def test_invalid_if_bad_password(self):
        """Shouldn't be valid if password change AND invalid old_password"""
        self.employee_data.update({'old_password': 'trucmuche'})
        user = User.objects.first()
        employee_form = EmployeeForm(self.employee_data, instance=user)
        self.assertFalse(employee_form.is_valid())
