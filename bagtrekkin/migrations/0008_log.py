# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0007_luggage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('horodator', models.DateTimeField(auto_now_add=True)),
                ('localisation', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(to='bagtrekkin.Employee')),
                ('flight', models.ForeignKey(to='bagtrekkin.Flight')),
                ('luggage', models.ForeignKey(to='bagtrekkin.Luggage')),
            ],
        ),
    ]
