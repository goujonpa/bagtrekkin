from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from tastypie.admin import ApiKeyInline

from bagtrekkin.models.airport import Airport
from bagtrekkin.models.company import Company
from bagtrekkin.models.employee import Employee
from bagtrekkin.models.eticket import Eticket
from bagtrekkin.models.flight import Flight
from bagtrekkin.models.log import Log
from bagtrekkin.models.luggage import Luggage
from bagtrekkin.models.passenger import Passenger


class EmployeeInline(admin.StackedInline):
    '''
    Define an inline admin descriptor for Employeemodel
    which acts a bit like a singleton
    '''
    model = Employee
    can_delete = False
    verbose_name_plural = 'employees'


class UserAdmin(UserAdmin):
    '''Define a new User admin with Employee and ApiKey attachhed'''
    inlines = (EmployeeInline, ApiKeyInline)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Basic registers
admin.site.register(Airport)
admin.site.register(Company)
admin.site.register(Passenger)
admin.site.register(Eticket)
admin.site.register(Luggage)
admin.site.register(Log)
admin.site.register(Flight)
admin.site.register(Employee)
