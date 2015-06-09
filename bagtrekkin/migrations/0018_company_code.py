# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0017_auto_20150608_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='code',
            field=models.CharField(default='', max_length=3),
            preserve_default=False,
        ),
    ]
