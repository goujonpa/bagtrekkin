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
