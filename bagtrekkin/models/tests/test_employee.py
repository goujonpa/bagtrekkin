from django.test import TestCase

from bagtrekkin.models.employee import Employee


class EmployeeTestCase(TestCase):
    fixtures = ['airports', 'companies', 'users', 'employees', 'passengers']

    def test_employee_unicode(self):
        '''Employee should be printed as expected'''
        employee = Employee.objects.first()
        self.assertEqual(unicode(employee), '%s - %s' % (employee.user.get_full_name(), employee.user.email))
