# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0027_auto_20150616_0243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=63)),
                ('city', models.CharField(max_length=63)),
                ('country', models.CharField(max_length=63)),
                ('code', models.CharField(unique=True, max_length=3)),
            ],
        ),
        migrations.RemoveField(
            model_name='log',
            name='localisation',
        ),
        migrations.AlterField(
            model_name='employee',
            name='district',
            field=models.CharField(max_length=63, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='function',
            field=models.CharField(blank=True, max_length=31, null=True, choices=[(b'checkin', b'Check-In'), (b'ramp', b'Ramp'), (b'lostfounds', b'Lost and Founds')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(blank=True, max_length=31, null=True, choices=[(b'pending', b'Pending'), (b'active', b'Active'), (b'blocked', b'Blocked')]),
        ),
        migrations.AddField(
            model_name='employee',
            name='airport',
            field=models.ForeignKey(blank=True, to='bagtrekkin.Airport', null=True),
        ),
    ]
