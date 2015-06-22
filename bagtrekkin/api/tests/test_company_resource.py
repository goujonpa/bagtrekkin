from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


class CompanyResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'company'
    fixtures = ['users', 'companies']
    fields = ['code', 'id', 'name', 'resource_uri']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()

    def test_get_schema_authorized(self):
        response, data = self.get_schema_authorized()
