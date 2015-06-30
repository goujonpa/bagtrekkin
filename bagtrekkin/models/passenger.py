from django.db import models

from bagtrekkin.models.constants import GENDERS


class Passenger(models.Model):
    email = models.CharField(max_length=254, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    pnr = models.CharField(max_length=6, unique=True)
    tel = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode('%s - %s' % (self.full_name, self.email))

    @property
    def full_name(self):
        '''Concatenate first and last name'''
        return '%s %s' % (self.first_name, self.last_name)
