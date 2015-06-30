from django.contrib.auth.models import User
from django.db import models

from bagtrekkin.models.airport import Airport
from bagtrekkin.models.company import Company
from bagtrekkin.models.flight import Flight

from bagtrekkin.models.constants import GENDERS, EMPLOYEE_FUNCTIONS, EMPLOYEE_STATUSES


class Employee(models.Model):
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    status = models.CharField(max_length=31, choices=EMPLOYEE_STATUSES, blank=True, null=True)
    function = models.CharField(max_length=31, choices=EMPLOYEE_FUNCTIONS, blank=True, null=True)
    airport = models.ForeignKey(Airport, blank=True, null=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    current_flight = models.ForeignKey(Flight, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return unicode('%s - %s' % (self.user.get_full_name(), self.user.email))
