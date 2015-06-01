# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0010_employee_passenger_property_renaming'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='company',
            field=models.ForeignKey(blank=True, to='bagtrekkin.Compagny', null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='district',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='function',
            field=models.CharField(blank=True, max_length=32, null=True, choices=[(b'checkin', b'Check-In'), (b'ramp', b'Ramp'), (b'lostfounds', b'Lost and Founds')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'm', b'M'), (b'f', b'F')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(blank=True, max_length=32, null=True, choices=[(b'pending', b'Pending'), (b'active', b'Active'), (b'blocked', b'Blocked')]),
        ),
    ]
