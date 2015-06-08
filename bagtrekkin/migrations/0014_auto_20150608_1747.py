# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0013_auto_20150608_1319'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'companies'},
        ),
        migrations.AlterModelOptions(
            name='eticket',
            options={'verbose_name_plural': 'etickets'},
        ),
        migrations.AlterModelOptions(
            name='flight',
            options={'verbose_name_plural': 'flights'},
        ),
        migrations.AlterModelOptions(
            name='log',
            options={'verbose_name_plural': 'logs'},
        ),
        migrations.AlterModelOptions(
            name='luggage',
            options={'verbose_name_plural': 'luggages'},
        ),
        migrations.AlterModelOptions(
            name='passenger',
            options={'verbose_name_plural': 'passengers'},
        ),
        migrations.AlterField(
            model_name='flight',
            name='duration',
            field=models.DurationField(),
        ),
    ]
