# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def load_stores_from_fixture(apps, schema_editor):
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "loaddata", "data_company"])


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0018_company_code'),
    ]

    operations = [
        migrations.RunPython(load_stores_from_fixture),
    ]
