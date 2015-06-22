from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


class EticketResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'eticket'
    fixtures = ['users', 'airports', 'companies', 'flights', 'passengers', 'etickets']
    fields = ['flights', 'id', 'passenger', 'resource_uri', 'summary', 'ticket_number']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()

    def test_get_schema_authorized(self):
        response, data = self.get_schema_authorized()
