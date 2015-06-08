# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0011_employee_null_authorized'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compagny',
            options={'verbose_name_plural': 'compagnies'},
        ),
        migrations.RemoveField(
            model_name='luggage',
            name='material',
        ),
        migrations.AddField(
            model_name='luggage',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 8, 16, 4, 43, 658214, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='luggage',
            name='is_already_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='luggage',
            name='material_number',
            field=models.CharField(default=0, max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'f', b'F'), (b'm', b'M')]),
        ),
        migrations.AlterField(
            model_name='luggage',
            name='passenger',
            field=models.ForeignKey(to='bagtrekkin.Passenger', null=True),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='gender',
            field=models.CharField(max_length=1, choices=[(b'f', b'F'), (b'm', b'M')]),
        ),
        migrations.DeleteModel(
            name='Material',
        ),
    ]
