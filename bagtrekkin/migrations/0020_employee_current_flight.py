# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0019_load_data_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='current_flight',
            field=models.ForeignKey(blank=True, to='bagtrekkin.Flight', null=True),
        ),
    ]
