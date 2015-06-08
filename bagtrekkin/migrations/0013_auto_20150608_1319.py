# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0012_auto_20150608_1305'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Compagny',
            new_name='Company',
        ),
    ]
