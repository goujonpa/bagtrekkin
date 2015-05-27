# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def load_stores_from_sql():
    from bagtrekkin.settings import BASE_DIR
    import os
    sql_statements = open(os.path.join(BASE_DIR, 'psql.sql'), 'r').read()
    return sql_statements


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(load_stores_from_sql()),
    ]
