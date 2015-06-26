from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


class EmployeeResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'employee'
    fixtures = ['users', 'employees', 'airports', 'companies']
    fields = [
        'current_flight', 'district', 'function',
        'gender', 'id', 'resource_uri', 'status', 'user',
    ]
    allowed_detail_http_methods = ['get', 'post']
    allowed_list_http_methods = ['get', 'post']

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
