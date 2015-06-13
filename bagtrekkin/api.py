from django.contrib.auth.models import User

from tastypie import fields
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from bagtrekkin.authorization import EmployeeObjectsOnlyAuthorization
from bagtrekkin.models import Company, Passenger, Flight, Employee, Eticket, Luggage, Log


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CompanyResource(ModelResource):

    class Meta:
        queryset = Company.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()


class PassengerResource(ModelResource):

    class Meta:
        queryset = Passenger.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()


class FlightResource(ModelResource):
    company = fields.ForeignKey(CompanyResource, 'company', full=True)
    etickets = fields.ManyToManyField('bagtrekkin.api.EticketResource', 'eticket_set')

    class Meta:
        queryset = Flight.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        filtering = {
            'airline': ALL
        }


class EmployeeResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', unique=True, readonly=True, full=True)
    current_flight = fields.ForeignKey(FlightResource, 'current_flight', blank=True, null=True, full=True)

    class Meta:
        queryset = Employee.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        authorization = EmployeeObjectsOnlyAuthorization()
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        excludes = ['token']
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
                'Only update on %s allowed' % ', '.join(
                    self._meta.allowed_update_fields
                )
            )
        try:
            flight_resource = FlightResource()
            flight_bundle = flight_resource.build_bundle(obj=Flight.from_airline(new_data['current_flight']))
            new_data['current_flight'] = flight_resource.get_resource_uri(flight_bundle)
        except Flight.DoesNotExist, e:
            new_data['current_flight'] = None
        return super(EmployeeResource, self).update_in_place(
            request, original_bundle, new_data
        )


class EticketResource(ModelResource):
    passenger = fields.ForeignKey(PassengerResource, 'passenger', full=True)
    flights = fields.ManyToManyField(FlightResource, 'flights', full=True)

    class Meta:
        queryset = Eticket.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())


class LuggageResource(ModelResource):
    passenger = fields.ForeignKey(PassengerResource, 'passenger', full=True)

    class Meta:
        queryset = Luggage.objects.all()
        allowed_methods = ['get', 'post']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        bundle = super(LuggageResource, self).obj_create(bundle, **kwargs)
        # if the bundle has correctly been saved we add a log
        if bundle.obj.pk:
            Log(
                employee=bundle.request.user.employee,
                luggage=bundle.obj
            ).save()
        return bundle


class LogResource(ModelResource):
    luggage = fields.ForeignKey(LuggageResource, 'luggage', full=True)
    employee = fields.ForeignKey(EmployeeResource, 'employee', full=True)
    flight = fields.ForeignKey(FlightResource, 'flight', full=True)

    class Meta:
        queryset = Log.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
