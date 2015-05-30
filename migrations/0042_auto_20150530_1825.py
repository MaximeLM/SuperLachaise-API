# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0041_auto_20150530_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCommandError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('type', models.CharField(max_length=255, verbose_name='type')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('admin_command', models.ForeignKey(to='superlachaise_api.AdminCommand')),
            ],
            options={
                'ordering': ['admin_command', 'type'],
                'verbose_name': 'admin command error',
                'verbose_name_plural': 'admin command errors',
            },
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='wikidata_combined',
            field=models.CharField(max_length=255, verbose_name='wikidata combined', blank=True),
        ),
    ]
