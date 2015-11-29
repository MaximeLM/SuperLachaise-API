# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0012_auto_20150623_0608'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('version_id', models.IntegerField(unique=True, verbose_name='version id', db_index=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'DB version',
                'verbose_name_plural': 'DB versions',
            },
        ),
    ]
