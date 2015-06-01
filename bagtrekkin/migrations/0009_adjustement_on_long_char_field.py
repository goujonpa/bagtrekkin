# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0008_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='token',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='flight',
            name='arrival_loc',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='flight',
            name='departure_loc',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='log',
            name='localisation',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='email',
            field=models.CharField(unique=True, max_length=254),
        ),
    ]
