from django.contrib.auth.models import User

from tastypie import fields, http
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource, Resource
from tastypie.utils import dict_strip_unicode_keys

from bagtrekkin.api.authorization import EmployeeObjectsOnlyAuthorization
from bagtrekkin.models import Company, Passenger, Flight, Employee, Eticket, Luggage, Log
from bagtrekkin.models import build_from_pnr_lastname_material_number


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
        allowed_methods = ['get', 'post']
        authorization = EmployeeObjectsOnlyAuthorization()
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


class EticketResource(ModelResource):
    passenger = fields.ForeignKey(PassengerResource, 'passenger')
    flights = fields.ManyToManyField(FlightResource, 'flights')

    class Meta:
        queryset = Eticket.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())


class LuggageResource(ModelResource):
    passenger = fields.ForeignKey(PassengerResource, 'passenger')

    class Meta:
        queryset = Luggage.objects.all()
        allowed_methods = ['get', 'post', 'patch', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        filtering = {
            'passenger': ALL
        }

    def obj_create(self, bundle, **kwargs):
        bundle = super(LuggageResource, self).obj_create(bundle, **kwargs)
        Log.create(
            user=bundle.request.user,
            luggage=bundle.obj,
        )
        return bundle

    def apply_filters(self, request, applicable_filters):
        try:
            if request.user.employee.current_flight:
                filters = Luggage.filters_from_flight(
                    request.user.employee.current_flight
                )
                return super(LuggageResource, self).apply_filters(
                    request, applicable_filters
                ).filter(**filters)
            else:
                raise BadRequest(
                    'Missing current_flight for current Employee. '
                    'Please set your current_flight first.'
                )
        except Employee.DoesNotExist:
            raise BadRequest(
                'Missing Employee Object for current User. '
                'Please create your profile on web the application.'
            )

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        data = dict_strip_unicode_keys(deserialized)
        if 'objects' not in data:
            raise BadRequest('Missing objects list.')
        base_bundle = self.build_bundle(request=request)
        supposed_objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        received_numbers = [obj['material_number'] for obj in data.get('objects')]
        if not received_numbers:
            raise BadRequest('Empty objects list.')
        received_filters = {'material_number__in': received_numbers}
        received_objects = self.get_object_list(request).filter(**received_filters)
        tp_objects = [obj for obj in received_objects if obj in supposed_objects]
        fn_objects = [obj for obj in received_objects if obj not in supposed_objects]
        fp_objects = [obj for obj in supposed_objects if obj not in received_objects]
        all_objects = {
            'tp': tp_objects,
            'fn': fn_objects,
            'fp': fp_objects
        }
        for status, objects in all_objects.iteritems():
            for obj in objects:
                Log.create(
                    user=request.user,
                    luggage=obj,
                    status=status
                )
        return http.HttpCreated()


class LogResource(ModelResource):
    luggage = fields.ForeignKey(LuggageResource, 'luggage', full=True)
    employee = fields.ForeignKey(EmployeeResource, 'employee', full=True)
    flight = fields.ForeignKey(FlightResource, 'flight', full=True)

    class Meta:
        queryset = Log.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()


class CheckinResource(Resource):

    class Meta:
        allowed_methods = ['post']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        request = bundle.request
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        if all(k in deserialized for k in ['pnr', 'last_name', 'material_number']):
            passenger, etickets, luggage = build_from_pnr_lastname_material_number(
                deserialized['pnr'],
                deserialized['last_name'],
                deserialized['material_number']
            )
            # if the luggage has correctly been saved, we can add a log
            # we take the flight from passenger eticket's first flight
            try:
                flight = [
                    flight
                    for e in etickets
                    for flight in e.flights.order_by('flight_date', 'departure_time')
                ][0]
            except IndexError:
                return http.HttpApplicationError(
                    'Application didn\'t find any flight for etickets.'
                )
            Log.create(user=request.user, luggage=luggage, flight=flight)
            return http.HttpCreated()
        else:
            return http.HttpApplicationError(
                'Missing pnr and/or last_name and/or material_number.'
            )

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        return kwargs
