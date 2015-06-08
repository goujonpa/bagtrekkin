from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from bagtrekkin.models import Luggage


class LuggagesResource(ModelResource):

    class Meta:
        queryset = Luggage.objects.all()
        resource_name = 'luggages'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(LuggagesResource, self).obj_create(bundle, request, **kwargs)
        Log(
            localisation=request.user.district,
            flight=request.user.current_flight,
            employee=request.user,
            luggage=bundle,
        ).save()
        return bundle
