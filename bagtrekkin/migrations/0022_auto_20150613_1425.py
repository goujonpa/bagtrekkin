# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0021_auto_20150609_0126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={},
        ),
        migrations.AlterField(
            model_name='flight',
            name='airline',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='luggage',
            name='passenger',
            field=models.ForeignKey(to='bagtrekkin.Passenger'),
        ),
    ]
