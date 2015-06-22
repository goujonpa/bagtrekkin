from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


class LogResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'log'
    fixtures = [
        'users', 'airports', 'companies', 'passengers',
        'flights', 'employees', 'luggages', 'logs'
    ]
    fields = ['datetime', 'employee', 'flight', 'id', 'luggage', 'resource_uri', 'status']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_schema_authorized(self):
        response, data = self.get_schema_authorized()
