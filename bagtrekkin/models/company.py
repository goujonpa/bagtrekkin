from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = "companies"

    def __unicode__(self):
        return unicode('%s - %s' % (self.name, self.code))
