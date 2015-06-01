# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0005_flight'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('material_number', models.CharField(max_length=16)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('is_already_read', models.BooleanField(default=False)),
            ],
        ),
    ]
