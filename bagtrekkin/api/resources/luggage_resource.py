from tastypie import fields, http
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie.utils import dict_strip_unicode_keys

from bagtrekkin.models.log import Log
from bagtrekkin.models.luggage import Luggage
from bagtrekkin.models.employee import Employee

from bagtrekkin.api.resources.passenger_resource import PassengerResource


class LuggageResource(ModelResource):
    passenger = fields.ForeignKey(PassengerResource, 'passenger')

    class Meta:
        queryset = Luggage.objects.all()
        allowed_methods = ['get', 'post']
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
        if not data.get('objects'):
            raise BadRequest('Empty objects list.')
        base_bundle = self.build_bundle(request=request)
        supposed_objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        received_numbers = [obj['material_number'] for obj in data.get('objects')]
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
