from django.test import TestCase
from django.contrib.auth.models import User

from bagtrekkin.forms.signup_form import SignupForm
from bagtrekkin.models.employee import Employee


class SignupFormTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'flights', 'users', 'employees', 'luggages', 'logs']

    def setUp(self):
        super(SignupFormTestCase, self).setUp()
        self.data = {
            'username': 'totodu33',
            'password1': 'tonton',
            'password2': 'tonton',
            'first_name': 'toto',
            'last_name': 'lebogoss',
            'email': 'totolebg@email.com'
        }
        self.form = SignupForm(self.data)

    def test_fields_required(self):
        '''Every field should be required'''
        self.assertTrue(self.form.fields['username'].required)
        self.assertTrue(self.form.fields['password1'].required)
        self.assertTrue(self.form.fields['password2'].required)
        self.assertTrue(self.form.fields['first_name'].required)
        self.assertTrue(self.form.fields['last_name'].required)
        self.assertTrue(self.form.fields['email'].required)

    def test_employee_is_created(self):
        '''Saving a form creates user AND employee LINKED to user'''
        if self.form.is_valid():
            self.form.save()
        user = User.objects.get(username='totodu33')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'totodu33')
        self.assertTrue(user.check_password, 'tonton')
        self.assertEqual(user.first_name, 'toto')
        self.assertEqual(user.last_name, 'lebogoss')
        self.assertEqual(user.email, 'totolebg@email.com')
        self.assertFalse(user.is_staff)
        employee = Employee.objects.get(user=user)
        self.assertIsInstance(employee, Employee)

    def test_username_already_exists_exception(self):
        '''An already existing username raises a validationerror'''
        if self.form.is_valid():
            self.form.save()
        form2 = SignupForm(self.data)
        self.assertFalse(form2.is_valid())
