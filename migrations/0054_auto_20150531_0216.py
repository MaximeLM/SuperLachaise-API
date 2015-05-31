# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0053_auto_20150531_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikipediapage',
            name='last_revision_id',
            field=models.CharField(max_length=255, verbose_name='last revision id', blank=True),
        ),
    ]
