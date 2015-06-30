from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


from bagtrekkin.forms.uk_error_list import UkErrorList
from bagtrekkin.models.constants import GENDERS, EMPLOYEE_FUNCTIONS
from bagtrekkin.models.airport import Airport
from bagtrekkin.models.company import Company
from bagtrekkin.models.employee import Employee


class ProfileForm(UserChangeForm):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    gender = forms.ChoiceField(choices=GENDERS, required=True)
    function = forms.ChoiceField(choices=EMPLOYEE_FUNCTIONS, required=True)
    airport = forms.ModelChoiceField(queryset=Airport.objects.all(), empty_label="(Choose an Airport)")
    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label="(Choose a Company)")
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        excludes = ('password', )

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['old_password'].required = False
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False
        if kwargs.get('instance') is None:
            raise AttributeError('No User instance provided to the employee form')
        try:
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['function'].initial = self.instance.employee.function
            self.fields['airport'].initial = self.instance.employee.airport
            self.fields['company'].initial = self.instance.employee.company
        except Employee.DoesNotExist:
            pass

    def clean_password(self):
        pass

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    "The two password fields didn't match.",
                    code='password_mismatch',
                )
        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if old_password:
            if not self.instance.check_password(old_password):
                raise forms.ValidationError(
                    "Your old password was entered incorrectly. Please enter it again.",
                    code='password_incorrect',
                )
        return old_password

    def save(self, commit=True):
        if self.cleaned_data.get('new_password1', None):
            self.instance.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.instance.save()
            self.instance.employee.gender = self.cleaned_data['gender']
            self.instance.employee.function = self.cleaned_data['function']
            self.instance.employee.airport = self.cleaned_data['airport']
            self.instance.employee.company = self.cleaned_data['company']
            self.instance.employee.save()
        return self.instance
