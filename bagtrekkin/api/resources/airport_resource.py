from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from bagtrekkin.models.airport import Airport


class AirportResource(ModelResource):

    class Meta:
        queryset = Airport.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
