# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0063_auto_20150601_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='attribution',
            field=models.CharField(max_length=255, verbose_name='attribution', blank=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='url',
            field=models.CharField(max_length=255, verbose_name='url', blank=True),
        ),
    ]
