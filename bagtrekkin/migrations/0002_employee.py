# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bagtrekkin', '0001_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullname', models.CharField(max_length=64)),
                ('district', models.CharField(max_length=64)),
                ('token', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=32, choices=[(b'pending', b'Pending'), (b'active', b'Active'), (b'blocked', b'Blocked')])),
                ('function', models.CharField(max_length=32, choices=[(b'checkin', b'Check-In')])),
                ('company', models.ForeignKey(to='bagtrekkin.Compagny')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
