# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def load_companies_from_fixture(apps, schema_editor):
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "loaddata", "companies"])


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0018_company_code'),
    ]

    operations = [
        migrations.RunPython(load_companies_from_fixture),
    ]
