# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0052_auto_20150531_0111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikipediapage',
            name='revision_id',
        ),
        migrations.AddField(
            model_name='wikipediapage',
            name='last_revision_id',
            field=models.CharField(default='', max_length=255, verbose_name='last revision id'),
            preserve_default=False,
        ),
    ]
