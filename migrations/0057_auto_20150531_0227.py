# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0056_auto_20150531_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikipediapage',
            name='last_revision_id',
            field=models.BigIntegerField(null=True, verbose_name='id derni\xe8re r\xe9vision'),
        ),
    ]
