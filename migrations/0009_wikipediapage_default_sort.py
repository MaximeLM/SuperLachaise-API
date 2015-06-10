# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0008_auto_20150609_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikipediapage',
            name='default_sort',
            field=models.CharField(max_length=255, verbose_name='default sort', blank=True),
        ),
    ]
