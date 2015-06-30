from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase
from bagtrekkin.models.employee import Employee
from bagtrekkin.models.flight import Flight
from bagtrekkin.models.log import Log
from bagtrekkin.models.luggage import Luggage


class LuggageResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'luggage'
    fixtures = ['users', 'passengers', 'airports', 'companies', 'luggages', 'etickets', 'employees', 'flights']
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

    def test_post_list_missing_objects_list(self):
        '''Should return an error missing objects list'''
        post_data = {}
        employee = Employee.objects.first()
        employee.current_flight = Flight.objects.get(airline='AR123')
        employee.save()
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpBadRequest(response)
        data = self.deserialize(response)
        self.assertKeys(data, ['error'])
        self.assertEqual(data['error'], 'Missing objects list.')

    def test_post_list_empty_objects_list(self):
        '''Should return an error empty objects list'''
        post_data = {
            'objects': []
        }
        employee = Employee.objects.first()
        employee.current_flight = Flight.objects.get(airline='AR123')
        employee.save()
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpBadRequest(response)
        data = self.deserialize(response)
        self.assertKeys(data, ['error'])
        self.assertEqual(data['error'], 'Empty objects list.')

    def test_post_list_ok(self):
        '''Should create True Positives, False Negatives, False Positives Logs'''
        post_data = {
            'objects': [
                {
                    'material_number': 'E200 6296 9619 0229 0370 EC2B'
                },
                {
                    'material_number': 'E983 0000 1111 2222 3333 4444'
                }
            ]
        }
        employee = Employee.objects.first()
        employee.current_flight = Flight.objects.get(airline='AR123')
        employee.save()
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpCreated(response)
        tps = Log.objects.filter(status='tp')
        fps = Log.objects.filter(status='fp')
        fns = Log.objects.filter(status='fn')
        self.assertIn(
            Log.objects.get(
                luggage=Luggage.objects.get(material_number='E200 6296 9619 0229 0370 EC2B')),
            tps
        )
        self.assertIn(
            Log.objects.get(
                luggage=Luggage.objects.get(material_number='E200 3411 B802 0115 1612 6723')),
            fps
        )
        self.assertIn(
            Log.objects.get(
                luggage=Luggage.objects.get(material_number='E983 0000 1111 2222 3333 4444')),
            fns
        )
