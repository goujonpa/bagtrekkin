# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0025_remove_luggage_is_already_read'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='horodator',
            new_name='datetime',
        ),
    ]
