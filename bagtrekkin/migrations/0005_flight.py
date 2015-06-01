# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0004_eticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('airline', models.CharField(max_length=6)),
                ('aircraft', models.CharField(max_length=64)),
                ('departure_loc', models.CharField(max_length=255)),
                ('departure_time', models.TimeField()),
                ('arrival_loc', models.CharField(max_length=255)),
                ('arrival_time', models.TimeField()),
                ('flight_date', models.DateField()),
                ('duration', models.TimeField()),
                ('company', models.ForeignKey(to='bagtrekkin.Compagny')),
                ('eticket', models.ForeignKey(to='bagtrekkin.Eticket')),
            ],
        ),
    ]
