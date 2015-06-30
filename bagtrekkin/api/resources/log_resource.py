from tastypie import fields
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from bagtrekkin.models.log import Log
from bagtrekkin.api.resources.employee_resource import EmployeeResource
from bagtrekkin.api.resources.flight_resource import FlightResource
from bagtrekkin.api.resources.luggage_resource import LuggageResource


class LogResource(ModelResource):
    luggage = fields.ForeignKey(LuggageResource, 'luggage', full=True)
    employee = fields.ForeignKey(EmployeeResource, 'employee', full=True)
    flight = fields.ForeignKey(FlightResource, 'flight', full=True)

    class Meta:
        queryset = Log.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
