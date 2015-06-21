from tastypie.api import Api

from bagtrekkin.api.resources import (
    UserResource, AirportResource, CompanyResource, PassengerResource,
    FlightResource, EmployeeResource, EticketResource, LuggageResource,
    LogResource, CheckinResource
)

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
