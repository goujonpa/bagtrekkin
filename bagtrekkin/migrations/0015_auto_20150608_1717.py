# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0014_auto_20150608_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='eticket',
        ),
        migrations.AddField(
            model_name='eticket',
            name='flights',
            field=models.ManyToManyField(to='bagtrekkin.Flight'),
        ),
    ]
