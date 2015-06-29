# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0030_log_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='district',
        ),
    ]
