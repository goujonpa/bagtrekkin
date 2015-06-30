from django.test import TestCase


class LogoutViewTestCase(TestCase):
    fixtures = ['airports', 'companies', 'users', 'employees']

    def test_logout(self):
        self.client.login(username='capflam', password='123')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get('/logout.html')
        self.assertRedirects(response, 'http://testserver/')
        self.assertNotIn('_auth_user_id', self.client.session)
