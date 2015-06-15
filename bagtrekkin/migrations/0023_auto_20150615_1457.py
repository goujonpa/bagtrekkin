# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0022_auto_20150613_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='luggage',
            name='material_number',
            field=models.CharField(max_length=30),
        ),
    ]
