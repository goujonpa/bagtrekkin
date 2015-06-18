# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def load_airports_from_fixture(apps, schema_editor):
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "loaddata", "airports"])


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0028_auto_20150618_0251'),
    ]

    operations = [
        migrations.RunPython(load_airports_from_fixture),
    ]
