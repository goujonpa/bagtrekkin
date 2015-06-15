# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0023_auto_20150615_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='current_flight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='bagtrekkin.Flight', null=True),
        ),
    ]
