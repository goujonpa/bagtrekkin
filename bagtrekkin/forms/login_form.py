from django.contrib.auth.forms import AuthenticationForm

from bagtrekkin.forms.uk_error_list import UkErrorList


class LoginForm(AuthenticationForm):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    def __init__(self, request=None, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(LoginForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True
