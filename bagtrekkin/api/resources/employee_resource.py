from tastypie import fields
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from bagtrekkin.api.authorizations.employee_authorization import EmployeeAuthorization
from bagtrekkin.models.employee import Employee
from bagtrekkin.models.flight import Flight
from bagtrekkin.api.resources.airport_resource import AirportResource
from bagtrekkin.api.resources.company_resource import CompanyResource
from bagtrekkin.api.resources.flight_resource import FlightResource
from bagtrekkin.api.resources.user_resource import UserResource


class EmployeeResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', unique=True, readonly=True, full=True)
    current_flight = fields.ForeignKey(FlightResource, 'current_flight', blank=True, null=True, full=True)
    airport = fields.ForeignKey(AirportResource, 'airport', blank=True, null=True, full=True)
    company = fields.ForeignKey(CompanyResource, 'company', blank=True, null=True, full=True)

    class Meta:
        queryset = Employee.objects.all()
        allowed_methods = ['get', 'post']
        authorization = EmployeeAuthorization()
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        allowed_update_fields = ['current_flight']
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        bundle = self.build_bundle(obj=bundle.request.user.employee, request=bundle.request)
        bundle = self.full_dehydrate(bundle)
        data = self.deserialize(bundle.request, bundle.request.body,
                                format=bundle.request.META.get('CONTENT_TYPE', 'application/json'))
        bundle_updated = self.update_in_place(bundle.request, bundle, data)
        return bundle_updated

    def obj_update(self, bundle, request=None, **kwargs):
        for field_name in self.fields:
            field = self.fields[field_name]

            if type(field) is fields.ForeignKey and field.null and bundle.data[field_name] is None:
                setattr(bundle.obj, field_name, None)

        return super(EmployeeResource, self).obj_update(bundle, **kwargs)

    def update_in_place(self, request, original_bundle, new_data):
        if set(new_data.keys()) - set(self._meta.allowed_update_fields):
            raise BadRequest(
                'Only update on %s allowed.' % ', '.join(
                    self._meta.allowed_update_fields
                )
            )
        try:
            flight_resource = FlightResource()
            flight_bundle = flight_resource.build_bundle(obj=Flight.get_from_airline(new_data['current_flight']))
            new_data['current_flight'] = flight_resource.get_resource_uri(flight_bundle)
        except Flight.DoesNotExist:
            new_data['current_flight'] = None
        return super(EmployeeResource, self).update_in_place(
            request, original_bundle, new_data
        )
