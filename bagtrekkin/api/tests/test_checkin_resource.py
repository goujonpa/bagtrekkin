from mock import patch, MagicMock

from bagtrekkin.api.tests.auth_resource_test_case import AuthResourceTestCase
from bagtrekkin.models import Employee, Passenger, Luggage, Flight, Eticket, Log


class CheckinResourceTestCase(AuthResourceTestCase):
    version = 'v1'
    resource = 'checkin'
    fixtures = [
        'users', 'airports', 'companies', 'passengers', 'etickets',
        'flights', 'employees', 'luggages', 'logs'
    ]
    fields = ['city', 'code', 'country', 'id', 'name', 'resource_uri']
    allowed_detail_http_methods = ['post']
    allowed_list_http_methods = ['post']
    return_from_request = {
        "etickets": [
            {
                "number": "000-2739560319",
                "summary": "Paris - Recife"
            },
            {
                "number": "000-2729056392",
                "summary": "Recife - Paris"
            }
        ],
        "flights": {
            "000-2729056392": [
                {
                    "aircraft": "Airbus Industrie A320",
                    "airline": "Tam Linhas Aereas JJ3505",
                    "arrival": {
                        "location": "Sao Paulo, Brazil - Guarulhos International, terminal 2",
                        "time": "21:00"
                    },
                    "date": "Sunday, May 10, 2015",
                    "departure": {
                        "location": "Recife, Brazil - Guararapes International",
                        "time": "17:30"
                    },
                    "duration": "3:30",
                    "summary": "Recife - Paris"
                },
                {
                    "aircraft": "Boeing 777-300",
                    "airline": "Tam Linhas Aereas JJ8084",
                    "arrival": {
                        "location": "London, United Kingdom - Heathrow, terminal 1",
                        "time": "15:10"
                    },
                    "date": "Sunday, May 10, 2015",
                    "departure": {
                        "location": "Sao Paulo, Brazil - Guarulhos International, terminal 3",
                        "time": "23:45"
                    },
                    "duration": "11:25",
                    "summary": "Recife - Paris"
                },
                {
                    "aircraft": "Airbus Industrie A319",
                    "airline": "British Airways BA336",
                    "arrival": {
                        "location": "Paris, France - Orly, terminal W",
                        "time": "18:55"
                    },
                    "date": "Sunday, May 10, 2015",
                    "departure": {
                        "location": "London, United Kingdom - Heathrow, terminal 5",
                        "time": "16:40"
                    },
                    "duration": "1:15",
                    "summary": "Recife - Paris"
                }
            ],
            "000-2739560319": [
                {
                    "aircraft": "Airbus Industrie A320",
                    "airline": "TAP Portugal TP433",
                    "arrival": {
                        "location": "Lisbon, Portugal - Airport, terminal 1",
                        "time": "14:40"
                    },
                    "date": "Sunday, April 26, 2015",
                    "departure": {
                        "location": "Paris, France - Orly, terminal W",
                        "time": "13:15"
                    },
                    "duration": "2:25",
                    "summary": "Paris - Recife"
                },
                {
                    "aircraft": "Airbus Industrie A330-200",
                    "airline": "TAP Portugal TP011",
                    "arrival": {
                        "location": "Recife, Brazil - Guararapes International",
                        "time": "20:40"
                    },
                    "date": "Sunday, April 26, 2015",
                    "departure": {
                        "location": "Lisbon, Portugal - Airport, terminal 1",
                        "time": "16:50"
                    },
                    "duration": "7:50",
                    "summary": "Paris - Recife"
                }
            ]
        },
        "passenger": {
            "email": "test@example.com",
            "fullname": "John Smith",
            "tel": "0987654321"
        },
        "status": "success"
    }

    def assert_before_api_call(self):
        self.assertEqual(Passenger.objects.count(), 2)
        self.assertEqual(Eticket.objects.count(), 1)
        self.assertEqual(Flight.objects.count(), 2)
        self.assertEqual(Luggage.objects.count(), 3)
        self.assertEqual(Log.objects.count(), 2)

    def test_post_unauthorized(self):
        '''Should return a unauthorized response'''
        post_data = {
            'pnr': 'FGH098',
            'last_name': 'Smith',
            'material_number': 'E487 3267 3298 4283 3291 8923'
        }
        response = self.api_client.post(self.endpoint, format='json', data=post_data)
        self.assertHttpUnauthorized(response)

    @patch('requests.get')
    def test_post_authorized_inexisting_pnr(self, mock_request):
        '''Should create Passenger, Etickets, Flights, Luggage and Log'''
        mock_response = MagicMock(
            json=MagicMock(return_value=self.return_from_request),
            status_code=200
        )
        mock_request.return_value = mock_response
        post_data = {
            'pnr': 'FGH098',
            'last_name': 'Smith',
            'material_number': 'E487 3267 3298 4283 3291 8923'
        }
        self.assert_before_api_call()
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpCreated(response)
        self.assertEqual(Passenger.objects.count(), 3)
        self.assertEqual(Eticket.objects.count(), 3)
        self.assertEqual(Flight.objects.count(), 7)
        self.assertEqual(Luggage.objects.count(), 4)
        self.assertEqual(Log.objects.count(), 3)
        log = Log.objects.last()
        self.assertIsInstance(log.employee, Employee)
        self.assertEqual(log.employee, self.user.employee)
        self.assertIsInstance(log.luggage, Luggage)
        self.assertEqual(log.luggage, Luggage.objects.get(material_number='E487 3267 3298 4283 3291 8923'))
        self.assertIsInstance(log.flight, Flight)
        self.assertEqual(log.flight, Flight.objects.get(airline='TP433'))

    @patch('requests.get')
    def test_post_authorized_existing_pnr(self, mock_request):
        '''Should only create Luggage and Log'''
        post_data = {
            'pnr': 'ABC123',
            'last_name': 'Smith',
            'material_number': 'E487 3267 3298 4283 6782 9314'
        }
        self.assert_before_api_call()
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpCreated(response)
        self.assertFalse(mock_request.called)
        self.assertEqual(Passenger.objects.count(), 2)
        self.assertEqual(Eticket.objects.count(), 1)
        self.assertEqual(Flight.objects.count(), 2)
        self.assertEqual(Luggage.objects.count(), 4)
        self.assertEqual(Log.objects.count(), 3)
        log = Log.objects.last()
        self.assertIsInstance(log.employee, Employee)
        self.assertEqual(log.employee, self.user.employee)
        self.assertIsInstance(log.luggage, Luggage)
        self.assertEqual(log.luggage, Luggage.objects.get(material_number='E487 3267 3298 4283 6782 9314'))
        self.assertIsInstance(log.flight, Flight)
        self.assertEqual(log.flight, Flight.objects.get(airline='AR123'))

    def test_post_authorized_luggage_already_exists(self):
        '''Should return an error luggage already exists'''
        post_data = {
            'pnr': 'ABC123',
            'last_name': 'Smith',
            'material_number': 'E200 6296 9619 0229 0370 EC2B'
        }
        self.assert_before_api_call()
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpBadRequest(response)
        data = self.deserialize(response)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Luggage already exists in database.')

    def test_post_authorized_missing_post_data(self):
        '''Should return an error missing post data'''
        post_data = {
            'pnr': 'ABC123'
        }
        self.assert_before_api_call()
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpBadRequest(response)
        data = self.deserialize(response)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing pnr and/or last_name and/or material_number.')

    @patch('bagtrekkin.api.resources.build_from_pnr_lastname_material_number')
    def test_post_authorized_flight_doesnt_exist(self, mock_build):
        '''Should return an error application didn't find any flight'''
        post_data = {
            'pnr': 'ABC123',
            'last_name': 'Smith',
            'material_number': 'E200 6296 5739 5302 4923 EC2B'
        }
        self.assert_before_api_call()
        mock_build.return_value = (None, [], None)
        auth = self.get_basic_auth()
        response = self.api_client.post(self.endpoint, format='json', data=post_data, authentication=auth)
        self.assertHttpBadRequest(response)
        data = self.deserialize(response)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Application didn\'t find any flight for etickets.')
