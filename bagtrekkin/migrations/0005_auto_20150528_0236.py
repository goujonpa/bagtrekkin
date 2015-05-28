# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0004_auto_20150528_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='materials',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 5, 36, 33, 185213, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logs',
            name='horodator',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='luggages',
            name='material_number',
            field=models.ForeignKey(to='bagtrekkin.Materials', db_column='id_material'),
        ),
    ]
