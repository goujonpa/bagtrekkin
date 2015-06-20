from tastypie.api import Api

from api.resources import (
    UserResource, CompanyResource, PassengerResource, FlightResource,
    EmployeeResource, EticketResource, LuggageResource, LogResource,
    CheckinResource
)

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(CompanyResource())
v1_api.register(PassengerResource())
v1_api.register(FlightResource())
v1_api.register(EmployeeResource())
v1_api.register(EticketResource())
v1_api.register(LuggageResource())
v1_api.register(LogResource())
v1_api.register(CheckinResource())
