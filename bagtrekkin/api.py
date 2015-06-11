from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from bagtrekkin.models import Luggage, Log, Flight


class LuggagesResource(ModelResource):

    class Meta:
        queryset = Luggage.objects.all()
        resource_name = 'luggage'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(LuggagesResource, self).obj_create(bundle, **kwargs)
        if bundle.obj.pk:
            Log(
                localisation=bundle.request.user.employee.district,
                flight=bundle.request.user.employee.current_flight,
                employee=bundle.request.user.employee,
                luggage=bundle.obj
            ).save()
        return bundle


class FlightsResource(ModelResource):

    class Meta:
        queryset = Flight.objects.all()
        resource_name = 'flight'
        allowed_methods = ['post', 'get']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
