# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0026_auto_20150616_0152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='token',
        ),
        migrations.RemoveField(
            model_name='luggage',
            name='datetime',
        ),
        migrations.AlterField(
            model_name='luggage',
            name='material_number',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]
