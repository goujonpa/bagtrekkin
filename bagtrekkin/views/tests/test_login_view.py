from django.test import TestCase


class LoginViewTestCase(TestCase):
    fixtures = ['airports', 'companies', 'users', 'employees']

    def test_login_get(self):
        with self.assertTemplateUsed('login.jade'):
            response = self.client.get('/login.html')
            self.assertEqual(response.status_code, 200)

    def test_login_post_invalid_no_field(self):
        self.client.login(username='capflam', password='123')
        with self.assertTemplateUsed('login.jade'):
            response = self.client.post('/login.html', {})
            self.assertEqual(response.status_code, 200)
            self.assertFormError(response, 'form', 'username', 'This field is required.')
            self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_login_post_successful(self):
        self.client.login(username='capflam', password='123')
        response = self.client.post('/login.html', {
            'username': 'capflam',
            'password': '123'
        })
        self.assertRedirects(response, 'http://testserver/search.html')
        self.assertIn('_auth_user_id', self.client.session)
