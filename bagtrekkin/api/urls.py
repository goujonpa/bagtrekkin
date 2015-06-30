from tastypie.api import Api

from bagtrekkin.api.resources.airport_resource import AirportResource
from bagtrekkin.api.resources.checkin_resource import CheckinResource
from bagtrekkin.api.resources.company_resource import CompanyResource
from bagtrekkin.api.resources.employee_resource import EmployeeResource
from bagtrekkin.api.resources.eticket_resource import EticketResource
from bagtrekkin.api.resources.flight_resource import FlightResource
from bagtrekkin.api.resources.log_resource import LogResource
from bagtrekkin.api.resources.luggage_resource import LuggageResource
from bagtrekkin.api.resources.passenger_resource import PassengerResource
from bagtrekkin.api.resources.user_resource import UserResource


bt_api = Api(api_name='v1')
bt_api.register(UserResource())
bt_api.register(AirportResource())
bt_api.register(CompanyResource())
bt_api.register(PassengerResource())
bt_api.register(FlightResource())
bt_api.register(EmployeeResource())
bt_api.register(EticketResource())
bt_api.register(LuggageResource())
bt_api.register(LogResource())
bt_api.register(CheckinResource())
