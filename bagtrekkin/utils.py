import requests

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from bagtrekkin.models.constants import GENDERS
from bagtrekkin.models.eticket import Eticket
from bagtrekkin.models.flight import Flight
from bagtrekkin.models.luggage import Luggage
from bagtrekkin.models.passenger import Passenger


def build_from_pnr_lastname_material_number(pnr, last_name, material_number):
    '''
    Build passenger, etickets list, luggage objects
    from PNR and Passenger Last Name
    '''
    try:
        passenger = Passenger.objects.get(pnr=pnr)
        etickets = passenger.eticket_set.all()
    except Passenger.DoesNotExist:
        headers = {'content-type': 'application/json'}
        url = 'http://alfredpnr.favrodd.com/find/%s/%s' % (pnr, last_name)
        response = requests.get(url, headers=headers)
        if response.status_code == requests.codes.ok:
            result = response.json()
            if result.get('status') and result.get('status') == 'success':
                full_name = result['passenger']['fullname']
                if 'mr' in full_name or 'Mr' in full_name:
                    gender = GENDERS[1][0]
                else:
                    gender = GENDERS[0][0]
                first_name = ' '.join(full_name.split(' ')[:-1])
                last_name = full_name.split(' ')[-1]
                passenger = Passenger(
                    email=result['passenger']['email'],
                    tel=result['passenger']['tel'],
                    first_name=first_name,
                    last_name=last_name,
                    pnr=pnr,
                    gender=gender
                )
                passenger.save()
                etickets = []
                for json_eticket in result['etickets']:
                    number = json_eticket['number']
                    summary = json_eticket['summary']
                    eticket = Eticket(
                        ticket_number=number,
                        summary=summary,
                        passenger=passenger,
                    )
                    try:
                        eticket.save()
                    except IntegrityError:
                        eticket = Eticket.objects.get(ticket_number=number)
                    etickets.append(eticket)
                    for json_flight in result['flights'][number]:
                        eticket.flights.add(Flight.get_from_json(json_flight))
            else:
                raise ValidationError(result)
        else:
            response.raise_for_status()
    luggage = Luggage(
        material_number=material_number,
        passenger=passenger
    )
    try:
        luggage.save()
    except IntegrityError:
        raise IntegrityError('Luggage already exists in database.')
    return passenger, etickets, luggage
