# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0024_auto_20150615_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='luggage',
            name='is_already_read',
        ),
    ]
