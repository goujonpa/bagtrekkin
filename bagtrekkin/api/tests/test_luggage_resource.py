from django.core.management import call_command

from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase
from bagtrekkin.models import Employee, Flight


class LuggageResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'luggage'
    fixtures = ['users', 'passengers', 'airports', 'companies', 'luggages', 'employees']
    fields = ['id', 'material_number', 'passenger', 'resource_uri']
    allowed_detail_http_methods = ['get', 'post']
    allowed_list_http_methods = ['get', 'post']

    def test_get_list_unauthorized(self):
        '''Should return unauthorized response'''
        self.get_list_unauthorized()

    def test_get_list_basic_auth_without_current_flight(self):
        '''Should return objects list based on Basic Authentication without Employee's current_flight'''
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
        '''Should return objects list based on ApiKey Authentication without Employee's current_flight'''
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

    def test_get_list_basic_auth_with_current_flight(self):
        '''Should return objects list based on ApiKey Authentication with Employee's current_flight'''
        call_command('loaddata', 'flights')
        employee = Employee.objects.first()
        employee.current_flight = Flight.objects.get(airline='AR123')
        employee.save()
        auth = self.get_basic_auth()
        response = self.api_client.get(self.endpoint, format='json', authentication=auth)
        self.assertValidJSONResponse(response)
        data = self.deserialize(response)
        self.assertKeys(data, ['meta', 'objects'])

    def test_get_schema_authorized(self):
        '''Should return appropriate schema based on Resource'''
        response, data = self.get_schema_authorized(['filtering'])

    def test_get_detail_basic_auth(self):
        '''Should return object details based on Basic Authentication'''
        response, data = self.get_detail_basic_auth()

    def test_get_detail_apikey_auth(self):
        '''Should return object details based on ApiKey Authentication'''
        response, data = self.get_detail_apikey_auth()
