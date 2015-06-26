from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


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

    def test_get_schema_authorized(self):
        '''Should return appropriate schema based on Resource'''
        response, data = self.get_schema_authorized(['filtering'])
