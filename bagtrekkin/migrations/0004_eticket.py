# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0003_passenger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket_number', models.CharField(unique=True, max_length=14)),
                ('summary', models.CharField(max_length=64)),
                ('passenger', models.ForeignKey(to='bagtrekkin.Passenger')),
            ],
        ),
    ]
