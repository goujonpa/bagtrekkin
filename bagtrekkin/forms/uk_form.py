from django import forms

from bagtrekkin.forms.uk_error_list import UkErrorList


class UkForm(forms.Form):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(UkForm, self).__init__(self, *args, **kwargs)
