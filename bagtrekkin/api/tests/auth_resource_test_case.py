from django.contrib.auth.models import User

from tastypie.test import ResourceTestCase


class AuthResourceTestCase(ResourceTestCase):
    version = 'v1'
    default_format = 'application/json'
    default_limit = 20
    allowed_detail_http_methods = ['get']
    allowed_list_http_methods = ['get']

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

    def get_schema_authorized(self, additional=[]):
        auth = self.get_apikey_auth()
        response = self.api_client.get('%sschema/' % self.endpoint, format='json', authentication=auth)
        self.assertHttpOK(response)
        data = self.deserialize(response)
        supposed = [
            'allowed_detail_http_methods', 'allowed_list_http_methods',
            'default_format', 'default_limit', 'fields'
        ] + additional
        self.assertKeys(data, supposed)
        self.assertEqual(data['default_format'], self.default_format)
        self.assertEqual(data['default_limit'], self.default_limit)
        self.assertEqual(data['allowed_list_http_methods'], self.allowed_list_http_methods)
        self.assertEqual(data['allowed_detail_http_methods'], self.allowed_detail_http_methods)
        self.assertKeys(data['fields'], self.fields)
        return response, data

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
        return response, data

    def get_list_basic_auth(self):
        auth = self.get_basic_auth()
        return self.get_list_authorized(auth)

    def get_list_apikey_auth(self):
        auth = self.get_apikey_auth()
        return self.get_list_authorized(auth)
