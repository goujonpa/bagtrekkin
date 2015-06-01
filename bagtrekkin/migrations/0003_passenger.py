# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0002_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('firstname', models.CharField(max_length=64)),
                ('lastname', models.CharField(max_length=64)),
                ('gender', models.CharField(max_length=1, choices=[(b'm', b'M'), (b'f', b'F')])),
                ('pnr', models.CharField(unique=True, max_length=6)),
                ('tel', models.CharField(max_length=20)),
            ],
        ),
    ]
