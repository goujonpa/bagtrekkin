# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0003_auto_20150527_2228'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materials',
            fields=[
                ('id_material', models.AutoField(serialize=False, primary_key=True)),
                ('material_number', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'materials',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='luggages',
            name='material_number',
        ),
    ]
