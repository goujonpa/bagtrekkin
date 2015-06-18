# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0029_auto_20150618_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='status',
            field=models.CharField(default='tp', max_length=31, choices=[(b'fp', b'False Positive'), (b'fn', b'False Negative'), (b'tp', b'True Positive')]),
            preserve_default=False,
        ),
    ]
