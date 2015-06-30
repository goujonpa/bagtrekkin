from django.contrib.auth.models import User
from django.db.models.signals import post_save

from tastypie.models import create_api_key

from bagtrekkin.models.employee import Employee


def create_employee(sender, instance, created, **kwargs):
    '''Signal to create an employee for every user creation'''
    if created and not kwargs.get('raw', False):
        employee, _ = Employee.objects.get_or_create(user=instance)
        employee.save()


post_save.connect(create_employee, sender=User)
post_save.connect(create_api_key, sender=User)
