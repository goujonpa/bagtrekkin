from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from tastypie.admin import ApiKeyInline

from bagtrekkin.models import Company
from bagtrekkin.models import Employee
from bagtrekkin.models import Passenger
from bagtrekkin.models import Eticket
from bagtrekkin.models import Luggage
from bagtrekkin.models import Log
from bagtrekkin.models import Flight


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employees'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (EmployeeInline, ApiKeyInline)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Basic registers
admin.site.register(Company)
admin.site.register(Passenger)
admin.site.register(Eticket)
admin.site.register(Luggage)
admin.site.register(Log)
admin.site.register(Flight)
