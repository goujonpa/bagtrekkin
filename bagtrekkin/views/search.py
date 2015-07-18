from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render

from bagtrekkin.forms.search_form import SearchForm
from bagtrekkin.models.log import Log
from bagtrekkin.models.luggage import Luggage
from bagtrekkin.models.passenger import Passenger


@login_required
def search(request):
    problematic_luggages = Log.objects.exclude(status='tp').order_by('-datetime')
    context = {'pbl': problematic_luggages}
    if not problematic_luggages:
        context.update({'error_pbl': 'No problematic luggage'})
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        context.update({
            'search_form': search_form,
            'active': 'search'
        })
        try:
            if search_form.is_valid():
                passenger, luggages, logs = search_form.search()
                context.update({
                    'passenger': passenger,
                    'luggages': luggages,
                    'logs': logs
                })
            else:
                context.update(csrf(request))
                return render(request, 'search.jade', context)
        except Luggage.DoesNotExist:
            context.update({'error_message': 'Luggages not found'})
        except Log.DoesNotExist:
            context.update({'error_message': 'Logs not found'})
        except Passenger.DoesNotExist:
            context.update({'error_message': 'Passenger not found'})
        context.update(csrf(request))
        return render(request, 'search.jade', context)
    if request.method == 'GET' and 'rfid' in request.GET:
        try:
            luggage = Luggage.objects.get(material_number=request.GET['rfid'])
            logs = Log.objects.filter(luggage=luggage).order_by('-datetime')
            context.update({
                'history_luggage': luggage,
                'history_logs': logs,
                'active': 'history'
            })
        except Luggage.DoesNotExist:
            context.update({'error_message': 'Luggage not found'})
        except Log.DoesNotExist:
            context.update({'error_message': 'Logs not found'})
    context.update({'search_form': SearchForm()})
    context.update(csrf(request))
    return render(request, 'search.jade', context)
