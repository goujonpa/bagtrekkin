from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from bagtrekkin.forms.uk_error_list import UkErrorList


class SignupForm(UserCreationForm):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
