from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


class EmployeeResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'employee'
    fixtures = ['users', 'employees', 'airports', 'companies', 'flights']
    fields = [
        'airport', 'company', 'current_flight', 'function',
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

    def test_get_detail_basic_auth(self):
        '''Should return object details based on Basic Authentication'''
        response, data = self.get_detail_basic_auth()

    def test_get_detail_apikey_auth(self):
        '''Should return object details based on ApiKey Authentication'''
        response, data = self.get_detail_apikey_auth()

    def test_set_current_flight(self):
        '''Should set the current_flight of Employee'''
        post_data = {
            'current_flight': 'AR123'
        }
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpCreated(response)
        data = self.deserialize(response)
        self.assertKeys(data, self.fields)
        self.assertIsNotNone(data['current_flight'])

    def test_flush_current_flight(self):
        '''Should flush the current_flight of Employee'''
        post_data = {
            'current_flight': ''
        }
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpCreated(response)
        data = self.deserialize(response)
        self.assertKeys(data, self.fields)
        self.assertIsNone(data['current_flight'])

    def test_update_not_allowed_field(self):
        '''Should return an errror only update authorized on allowed fields'''
        post_data = {
            'function': 'ramp'
        }
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpBadRequest(response)
        data = self.deserialize(response)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Only update on current_flight allowed.')
