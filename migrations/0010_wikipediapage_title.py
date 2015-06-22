# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0009_auto_20150623_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikipediapage',
            name='title',
            field=models.CharField(default='title', max_length=255, verbose_name='title'),
            preserve_default=False,
        ),
    ]
