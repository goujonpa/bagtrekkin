# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0020_employee_current_flight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='airline',
            field=models.CharField(unique=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'f', b'F'), (b'm', b'M')]),
        ),
    ]
