from tastypie import http
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource

from bagtrekkin.models.log import Log
from bagtrekkin.utils import build_from_pnr_lastname_material_number


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
        if all([k in deserialized for k in ['pnr', 'last_name', 'material_number']]):
            passenger, etickets, luggage = build_from_pnr_lastname_material_number(
                deserialized['pnr'],
                deserialized['last_name'],
                deserialized['material_number']
            )
            # if the luggage has correctly been saved, we can add a log
            # we take the flight from passenger eticket's first flight
            try:
                # TODO https://github.com/goujonpa/bagtrekkin/issues/30
                # This should take into consideration flight dates
                # in etickets and take the closer flight from today
                flight = [
                    flight
                    for e in etickets
                    for flight in e.flights.order_by('flight_date', 'departure_time')
                ][0]
            except IndexError:
                raise IndexError(
                    'Application didn\'t find any flight for etickets.'
                )
            Log.create(user=request.user, luggage=luggage, flight=flight)
            return http.HttpCreated()
        else:
            raise ValueError(
                'Missing pnr and/or last_name and/or material_number.'
            )

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        return kwargs
