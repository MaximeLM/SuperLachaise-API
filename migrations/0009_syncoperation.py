# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0008_auto_20150526_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyncOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(max_length=255)),
                ('last_executed', models.DateTimeField(null=True)),
                ('last_result', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
