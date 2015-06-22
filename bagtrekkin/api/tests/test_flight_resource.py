from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


class FlightResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'flight'
    fixtures = ['users', 'companies', 'flights']
    fields = [
        'aircraft', 'airline', 'arrival_loc', 'arrival_time', 'company',
        'departure_loc', 'departure_time', 'duration', 'etickets',
        'flight_date', 'id', 'resource_uri'
    ]

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()

    def test_get_schema_authorized(self):
        response, data = self.get_schema_authorized(['filtering'])
