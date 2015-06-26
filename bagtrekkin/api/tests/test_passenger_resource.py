from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


class PassengerResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'passenger'
    fixtures = ['users', 'passengers']
    fields = ['email', 'first_name', 'gender', 'id', 'last_name', 'pnr', 'resource_uri', 'tel']

    def test_get_list_unauthorized(self):
        '''Should return unauthorized response'''
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        '''Should return objects list based on Basic Authentication'''
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        '''Should return objects list based on ApiKey Authentication'''
        response, data = self.get_list_apikey_auth()

    def test_get_schema_authorized(self):
        '''Should return appropriate schema based on Resource'''
        response, data = self.get_schema_authorized()
