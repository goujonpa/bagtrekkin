from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms.utils import ErrorList

from bagtrekkin.models import GENDER_CHOICES, STATUS_CHOICES, FUNCTION_CHOICES
from bagtrekkin.models import Employee, Company, Passenger, Luggage, Flight


class UkErrorList(ErrorList):

    def __unicode__(self):
        return self.as_uk_list()

    def as_uk_list(self):
        if not self:
            return ''
        return '<span class="">%s</span>' % ''.join([e for e in self])


class UkForm(forms.Form):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(UkForm, self).__init__(self, *args, **kwargs)


class CurrentFlightForm(forms.Form):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    flight = forms.ModelChoiceField(required=True, label='Flight Number', queryset=Flight.potentials())

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(CheckinForm, self).__init__(*args, **kwargs)


class CheckinForm(forms.Form):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    pnr = forms.CharField(required=True, label='Passenger Name Record')
    name = forms.CharField(required=True, label='Passenger Name')
    material_number = forms.ModelChoiceField(required=True, label='Material Number', queryset=Luggage.unreads())

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(CheckinForm, self).__init__(*args, **kwargs)


class FormSearch(forms.Form):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    pnr = forms.CharField(required=False, label='Passenger Name Record')
    material_number = forms.CharField(required=False, label='Material Number')

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(FormSearch, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        pnr = cleaned_data.get('pnr')
        material = cleaned_data.get('material_number')
        if not pnr and material_number:
            msg = 'No value provided'
            self.add_error('Error', msg)
        return cleaned_data

    def search(self):
        pnr = self.cleaned_data.get('pnr')
        material_number = self.cleaned_data.get('material_number')
        if pnr is not None:
            passenger = Passenger.objects.get(pnr=pnr)
        elif material is not None:
            material = Material.objects.get(material_number=material_number)


class FormEmployee(UserChangeForm):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    function = forms.ChoiceField(choices=FUNCTION_CHOICES, required=True)
    district = forms.CharField(max_length=64, required=True)
    company = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label="(Choose a Company)")
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New password confirmation", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(FormEmployee, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['old_password'].required = False
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False
        try:
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['function'].initial = self.instance.employee.function
            self.fields['district'].initial = self.instance.employee.district
            self.fields['company'].initial = self.instance.employee.company
        except Employee.DoesNotExist:
            pass

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        excludes = ('password', )

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
            self.instance.employee.district = self.cleaned_data['district']
            self.instance.employee.company = self.cleaned_data['company']
            self.instance.employee.save()
        return self.instance


class FormSignup(UserCreationForm):
    error_css_class = 'uk-form-danger'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': UkErrorList})
        super(FormSignup, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
