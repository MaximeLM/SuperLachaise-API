# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0004_auto_20150616_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openstreetmapwikipediatag',
            name='language_code',
            field=models.CharField(max_length=255, verbose_name='language code'),
        ),
        migrations.AlterField(
            model_name='openstreetmapwikipediatag',
            name='wikipedia',
            field=models.CharField(max_length=255, verbose_name='wikipedia'),
        ),
    ]
