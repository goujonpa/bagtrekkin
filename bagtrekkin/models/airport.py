from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=63)
    city = models.CharField(max_length=63)
    country = models.CharField(max_length=63)
    code = models.CharField(max_length=3, unique=True)

    def __unicode__(self):
        return unicode('%s (%s) - %s' % (self.name, self.code, self.country))
