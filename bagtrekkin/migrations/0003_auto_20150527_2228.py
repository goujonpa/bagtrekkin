# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrekkin', '0002_create_user_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compagnies',
            fields=[
                ('id_company', models.AutoField(default=1, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'compagnies',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id_employee', models.AutoField(default=1, serialize=False, primary_key=True)),
                ('cpf', models.CharField(unique=True, max_length=255)),
                ('function', models.CharField(max_length=255, choices=[(b'Mulher do check-in', b'Mulher do check-in')])),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255, choices=[(b'Pendente', b'Pendente'), (b'Ativo', b'Ativo'), (b'Dispensado', b'Dispensado')])),
                ('token', models.CharField(default=None, max_length=255, null=True)),
                ('district', models.CharField(max_length=255)),
                ('id_company', models.ForeignKey(to='bagtrekkin.Compagnies', db_column='id_company')),
            ],
            options={
                'db_table': 'employees',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Etickets',
            fields=[
                ('id_eticket', models.AutoField(serialize=False, primary_key=True)),
                ('ticket_number', models.CharField(unique=True, max_length=255)),
                ('summary', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'etickets',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('id_flight', models.AutoField(serialize=False, primary_key=True)),
                ('aircraft', models.CharField(max_length=255)),
                ('airline', models.CharField(max_length=255)),
                ('departure_loc', models.CharField(max_length=255)),
                ('departure_time', models.TimeField()),
                ('arrival_loc', models.CharField(max_length=255)),
                ('arrival_time', models.TimeField()),
                ('flight_date', models.DateField()),
                ('duration', models.TimeField()),
                ('id_company', models.ForeignKey(to='bagtrekkin.Compagnies', db_column='id_company')),
                ('id_eticket', models.ForeignKey(to='bagtrekkin.Etickets', db_column='id_eticket')),
            ],
            options={
                'db_table': 'flights',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id_log', models.IntegerField(serialize=False, primary_key=True)),
                ('horodator', models.DateTimeField()),
                ('localisation', models.CharField(default=None, max_length=255, null=True)),
                ('id_employee', models.ForeignKey(to='bagtrekkin.Employees', db_column='id_employee')),
                ('id_flight', models.ForeignKey(to='bagtrekkin.Flights', db_column='id_flight')),
            ],
            options={
                'db_table': 'logs',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Luggages',
            fields=[
                ('id_luggage', models.AutoField(serialize=False, primary_key=True)),
                ('material_number', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'luggages',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Passengers',
            fields=[
                ('id_user', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('pnr', models.CharField(unique=True, max_length=255)),
                ('tel', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'passengers',
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'managed': True},
        ),
        migrations.AddField(
            model_name='luggages',
            name='id_passenger',
            field=models.ForeignKey(to='bagtrekkin.Passengers', db_column='id_passenger'),
        ),
        migrations.AddField(
            model_name='logs',
            name='id_luggage',
            field=models.ForeignKey(to='bagtrekkin.Luggages', db_column='id_luggage'),
        ),
        migrations.AddField(
            model_name='etickets',
            name='id_passenger',
            field=models.ForeignKey(to='bagtrekkin.Passengers', db_column='id_passenger'),
        ),
    ]
