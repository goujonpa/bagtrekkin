from django.contrib.auth.models import User
from django.test import TestCase


class LoginViewTestCase(TestCase):
    fixtures = ['airports', 'companies', 'users', 'employees']

    def test_login_get(self):
        with self.assertTemplateUsed('login.jade'):
            response = self.client.get('/login.html')
            self.assertEqual(response.status_code, 200)

    def test_login_post_invalid_no_field(self):
        pass
