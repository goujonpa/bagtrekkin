from django import forms

from bagtrekkin.forms.uk_error_list import UkErrorList
from bagtrekkin.models.log import Log
from bagtrekkin.models.luggage import Luggage
from bagtrekkin.models.passenger import Passenger


class SearchForm(forms.Form):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    pnr = forms.CharField(required=False, label='Passenger Name Record')
    material_number = forms.CharField(required=False, label='Material Number')

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(SearchForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        pnr = cleaned_data.get('pnr')
        material_number = cleaned_data.get('material_number')

        if not (pnr or material_number):
            raise forms.ValidationError('Please fill one field')
        if pnr and material_number:
            raise forms.ValidationError('Please only fill one field')
        return cleaned_data

    def search(self):
        pnr = self.cleaned_data.get('pnr')
        material_number = self.cleaned_data.get('material_number')
        if pnr:
            passenger = Passenger.objects.get(pnr=pnr)
        elif material_number:
            passenger = Luggage.objects.get(material_number=material_number).passenger
        luggages = Luggage.objects.filter(passenger=passenger)
        logs = Log.objects.filter(luggage__passenger=passenger).order_by('-datetime')
        return passenger, luggages, logs
