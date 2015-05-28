# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0005_auto_20150528_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='materials',
            name='is_already_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='logs',
            name='localisation',
            field=models.CharField(default=datetime.datetime(2015, 5, 28, 9, 26, 39, 287397, tzinfo=utc), max_length=255, blank=True),
            preserve_default=False,
        ),
    ]
