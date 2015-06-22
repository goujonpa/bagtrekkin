from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


class PassengerResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'passenger'
    fixtures = ['users', 'passengers']
    fields = ['email', 'first_name', 'gender', 'id', 'last_name', 'pnr', 'resource_uri', 'tel']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()

    def test_get_schema_authorized(self):
        response, data = self.get_schema_authorized()
