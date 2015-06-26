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
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()

    def test_get_schema_authorized(self):
        response, data = self.get_schema_authorized()
