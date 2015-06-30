from django.contrib.auth.models import User
from django.test import TestCase

from bagtrekkin.forms.profile_form import ProfileForm
from bagtrekkin.models.employee import Employee


class ProfileFormTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'flights', 'users', 'employees', 'luggages', 'logs']

    def setUp(self):
        super(ProfileFormTestCase, self).setUp()
        self.employee_data = {
            'username': 'capflam',
            'first_name': 'Capitain',
            'last_name': 'Flamme',
            'email': 'ariane@space.com',
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
        '''Basic save should work'''
        user = User.objects.first()
        employee_form = ProfileForm(self.employee_data, instance=user)
        self.assertTrue(employee_form.is_valid())
        employee_form.save()
        employee = Employee.objects.get(user=user)
        self.assertIsInstance(employee, Employee)
        self.assertEqual(user.username, 'capflam')
        self.assertTrue(user.check_password('soleil'))
        self.assertEqual(employee.airport.code, 'CQF')
        self.assertEqual(employee.company.code, 'RBU')
        self.assertEqual(employee.gender, 'f')
        self.assertEqual(employee.function, 'ramp')

    def test_init_without_instance_parameter(self):
        '''Not passing an instance should raise an error'''
        with self.assertRaises(AttributeError):
            ProfileForm()
        with self.assertRaises(AttributeError):
            ProfileForm(self.employee_data)

    def test_invalid_if_bad_password(self):
        '''Shouldn't be valid if password change AND invalid old_password'''
        self.employee_data.update({'old_password': 'trucmuche'})
        user = User.objects.first()
        employee_form = ProfileForm(self.employee_data, instance=user)
        self.assertFalse(employee_form.is_valid())

    def test_invalid_if_diff_new_pwd(self):
        '''Shouldn't be valid if new passwords are differents'''
        self.employee_data.update({'new_password1': 'trucmuche'})
        user = User.objects.first()
        employee_form = ProfileForm(self.employee_data, instance=user)
        self.assertFalse(employee_form.is_valid())

    def test_invalid_if_false_airport(self):
        '''Shouldn't be valid if airport index not in available range'''
        self.employee_data.update({'airport': '1000'})
        user = User.objects.first()
        employee_form = ProfileForm(self.employee_data, instance=user)
        self.assertFalse(employee_form.is_valid())

    def test_invalid_if_false_company(self):
        '''Shouldn't be valid if company index not in available range'''
        self.employee_data.update({'company': '1000'})
        user = User.objects.first()
        employee_form = ProfileForm(self.employee_data, instance=user)
        self.assertFalse(employee_form.is_valid())
