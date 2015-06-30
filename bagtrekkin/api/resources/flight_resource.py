from tastypie import fields
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.resources import ModelResource

from bagtrekkin.models.flight import Flight
from bagtrekkin.api.resources.company_resource import CompanyResource


class FlightResource(ModelResource):
    company = fields.ForeignKey(CompanyResource, 'company', full=True)
    etickets = fields.ManyToManyField('bagtrekkin.api.resources.eticket_resource.EticketResource', 'eticket_set')

    class Meta:
        queryset = Flight.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        filtering = {
            'airline': ALL
        }
