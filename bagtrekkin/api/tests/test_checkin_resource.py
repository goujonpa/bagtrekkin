from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase


class AirportResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'checkin'
    fixtures = [
        'users', 'airports', 'companies', 'passengers',
        'flights', 'employees', 'luggages', 'logs'
    ]
    fields = ['city', 'code', 'country', 'id', 'name', 'resource_uri']
    allowed_detail_http_methods = ['post']
    allowed_list_http_methods = ['post']
    post_data = {
        'pnr': 'ABC123',
        'last_name': 'Raimbaud',
        'material_number': 'E200 2996 9618 0246 2230 2CD7'
    }

    def test_post_unauthorized(self):
        response = self.api_client.post(self.endpoint, format='json', data=self.post_data)
        self.assertHttpUnauthorized(response)
