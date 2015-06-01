# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0006_material'),
    ]

    operations = [
        migrations.CreateModel(
            name='Luggage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('material', models.ForeignKey(to='bagtrekkin.Material')),
                ('passenger', models.ForeignKey(to='bagtrekkin.Passenger')),
            ],
        ),
    ]
