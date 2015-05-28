# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0006_auto_20150528_0626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='luggages',
            old_name='material_number',
            new_name='id_material',
        ),
    ]
