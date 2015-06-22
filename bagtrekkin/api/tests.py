from django.contrib.auth.models import User

from tastypie.test import ResourceTestCase


class SchemaResourceTestCase(ResourceTestCase):
    def test_api_schema(self):
        response = self.api_client.get('/api/v1/', format='json')
        self.assertHttpOK(response)
        self.assertKeys(self.deserialize(response), [
            'airport', 'checkin', 'company', 'employee',
            'eticket', 'flight', 'log', 'luggage', 'passenger',
            'user'
        ])


class AuthResourceTestCase(ResourceTestCase):
    def setUp(self):
        super(AuthResourceTestCase, self).setUp()
        self.username = 'capflam'
        self.password = '123'
        self.user = User.objects.get(username=self.username)
        self.apikey = self.user.api_key.key
        self.endpoint = '/api/%s/%s/' % (self.version, self.resource)

    def get_basic_auth(self):
        return self.create_basic(self.username, self.password)

    def get_apikey_auth(self):
        return self.create_apikey(self.username, self.apikey)

    def get_list_unauthorized(self):
        response = self.api_client.get(self.endpoint, format='json')
        self.assertHttpUnauthorized(response)
        data = self.deserialize(response)
        return response, data

    def get_list_authorized(self, auth):
        response = self.api_client.get(self.endpoint, format='json', authentication=auth)
        self.assertHttpOK(response)
        data = self.deserialize(response)
        self.assertKeys(data, ['meta', 'objects'])
        self.assertGreaterEqual(len(data['objects']), 1)
        self.assertKeys(data['objects'][0], self.keys)
        return response, data

    def get_list_basic_auth(self):
        auth = self.get_basic_auth()
        return self.get_list_authorized(auth)

    def get_list_apikey_auth(self):
        auth = self.get_apikey_auth()
        return self.get_list_authorized(auth)


class UserResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'user'
    fixtures = ['users']
    keys = ['email', 'first_name', 'id', 'last_name', 'resource_uri', 'username']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()


class AirportResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'airport'
    fixtures = ['users', 'airports']
    keys = ['city', 'code', 'country', 'id', 'name', 'resource_uri']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()


class CompanyResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'company'
    fixtures = ['users', 'companies']
    keys = ['code', 'id', 'name', 'resource_uri']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()


class PassengerResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'passenger'
    fixtures = ['users', 'passengers']
    keys = ['email', 'first_name', 'gender', 'id', 'last_name', 'pnr', 'resource_uri', 'tel']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()


class FlightResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'flight'
    fixtures = ['users', 'companies', 'flights']
    keys = [
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


class EmployeeResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'employee'
    fixtures = ['users', 'employees', 'airports', 'companies']
    keys = [
        'current_flight', 'district', 'function',
        'gender', 'id', 'resource_uri', 'status', 'user',
    ]

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()


class EticketResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'eticket'
    fixtures = ['users', 'airports', 'companies', 'flights', 'passengers', 'etickets']
    keys = ['flights', 'id', 'passenger', 'resource_uri', 'summary', 'ticket_number']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()


class LuggageResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'luggage'
    fixtures = ['users', 'passengers', 'airports', 'companies', 'luggages', 'employees']
    keys = ['id', 'material_number', 'passenger', 'resource_uri']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth_without_current_flight(self):
        auth = self.get_basic_auth()
        response = self.api_client.get(self.endpoint, format='json', authentication=auth)
        self.assertHttpBadRequest(response)
        data = self.deserialize(response)
        self.assertKeys(data, ['error'])
        self.assertEqual(
            data['error'],
            'Missing current_flight for current Employee. '
            'Please set your current_flight first.'
        )

    def test_get_list_apikey_auth_without_current_flight(self):
        auth = self.get_apikey_auth()
        response = self.api_client.get(self.endpoint, format='json', authentication=auth)
        self.assertHttpBadRequest(response)
        data = self.deserialize(response)
        self.assertKeys(data, ['error'])
        self.assertEqual(
            data['error'],
            'Missing current_flight for current Employee. '
            'Please set your current_flight first.'
        )


class LogResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'log'
    fixtures = [
        'users', 'airports', 'companies', 'passengers',
        'flights', 'employees', 'luggages', 'logs'
    ]
    keys = ['datetime', 'employee', 'flight', 'id', 'luggage', 'resource_uri', 'status']

    def test_get_list_unauthorized(self):
        self.get_list_unauthorized()

    def test_get_list_basic_auth(self):
        response, data = self.get_list_basic_auth()
        self.assertKeys(data, ['meta', 'objects'])
        self.assertGreaterEqual(len(data['objects']), 1)
        self.assertKeys(data['objects'][0], self.keys)

    def test_get_list_apikey_auth(self):
        response, data = self.get_list_apikey_auth()
        self.assertKeys(data, ['meta', 'objects'])
        self.assertGreaterEqual(len(data['objects']), 1)
        self.assertKeys(data['objects'][0], self.keys)

