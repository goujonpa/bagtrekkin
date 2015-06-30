from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from bagtrekkin.models.passenger import Passenger


class PassengerResource(ModelResource):

    class Meta:
        queryset = Passenger.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
