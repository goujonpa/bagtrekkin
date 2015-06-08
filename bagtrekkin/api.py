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
