# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0009_adjustement_on_long_char_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passenger',
            old_name='firstname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='passenger',
            old_name='lastname',
            new_name='last_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='fullname',
        ),
        migrations.AddField(
            model_name='employee',
            name='gender',
            field=models.CharField(default='M', max_length=1, choices=[(b'm', b'M'), (b'f', b'F')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='function',
            field=models.CharField(max_length=32, choices=[(b'checkin', b'Check-In'), (b'ramp', b'Ramp'), (b'lostfounds', b'Lost and Founds')]),
        ),
    ]
