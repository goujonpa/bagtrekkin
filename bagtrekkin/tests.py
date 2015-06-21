from django.test import TestCase
from bagtrekkin.models import Airport, Company, Passenger, Flight, Employee, Eticket, Luggage, Log


class AirportTestCase(TestCase):
    fixtures = ['airports']

    def test_airport_unicode(self):
        """Airport should be printed as expected"""
        airport = Airport.objects.first()
        self.assertEqual(unicode(airport), '%s (%s) - %s' % (airport.name, airport.code, airport.country))


class CompanyTestCase(TestCase):
    fixtures = ['companies']

    def test_company_unicode(self):
        """Company should be printed as expected"""
        company = Company.objects.first()
        self.assertEqual(unicode(company), '%s - %s' % (company.name, company.code))


class PassengerTestCase(TestCase):
    fixtures = ['passengers']

    def test_passenger_full_name(self):
        """Passenger should be printed as expected"""
        passenger = Passenger.objects.first()
        self.assertEqual(passenger.full_name, '%s %s' % (passenger.first_name, passenger.last_name))

    def test_passenger_unicode(self):
        """Passenger should be printed as expected"""
        passenger = Passenger.objects.first()
        self.assertEqual(unicode(passenger), '%s - %s' % (passenger.full_name, passenger.email))


class FlightTestCase(TestCase):
    fixtures = ['companies', 'flights']

    def test_flight_unicode(self):
        """Flight should be printed as expected"""
        flight = Flight.objects.first()
        self.assertEqual(unicode(flight), '%s - %s - %s' % (flight.airline, flight.company, flight.flight_date))


class EmployeeTestCase(TestCase):
    fixtures = ['airports', 'companies', 'users', 'employees']

    def test_employee_unicode(self):
        """Employee should be printed as expected"""
        employee = Employee.objects.first()
        self.assertEqual(unicode(employee), '%s - %s' % (employee.user.get_full_name(), employee.user.email))


class EticketTestCase(TestCase):
    fixtures = ['companies', 'flights', 'passengers', 'etickets']

    def test_eticket_unicode(self):
        """Eticket should be printed as expected"""
        eticket = Eticket.objects.first()
        self.assertEqual(unicode(eticket), '%s - %s' % (eticket.passenger, eticket.ticket_number))


class LuggageTestCase(TestCase):
    fixtures = ['passengers', 'luggages']

    def test_luggage_unicode(self):
        """Luggage should be printed as expected"""
        luggage = Luggage.objects.first()
        self.assertEqual(unicode(luggage), '%s' % (luggage.material_number))


class LogTestCase(TestCase):
    fixtures = ['airports', 'companies', 'passengers', 'flights', 'users', 'employees', 'luggages', 'logs']

    def test_log_unicode(self):
        """Log should be printed as expected"""
        log = Log.objects.first()
        self.assertEqual(unicode(log), '%s (%s) - %s - %s' % (
            log.airport, log.stage, log.luggage, log.datetime.strftime('%d, %b %Y @ %H:%m')
        ))
