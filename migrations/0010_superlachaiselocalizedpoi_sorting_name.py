# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0009_wikipediapage_default_sort'),
    ]

    operations = [
        migrations.AddField(
            model_name='superlachaiselocalizedpoi',
            name='sorting_name',
            field=models.CharField(default='sorting name', max_length=255, verbose_name='nom pour tri'),
            preserve_default=False,
        ),
    ]
