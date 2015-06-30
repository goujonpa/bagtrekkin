from tastypie import fields
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.resources import ModelResource

from bagtrekkin.models.eticket import Eticket
from bagtrekkin.api.resources.flight_resource import FlightResource
from bagtrekkin.api.resources.passenger_resource import PassengerResource


class EticketResource(ModelResource):
    passenger = fields.ForeignKey(PassengerResource, 'passenger')
    flights = fields.ManyToManyField(FlightResource, 'flights')

    class Meta:
        queryset = Eticket.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
