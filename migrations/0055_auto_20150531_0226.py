# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0054_auto_20150531_0216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikipediapage',
            name='last_revision_id',
        ),
        migrations.AddField(
            model_name='wikipediapage',
            name='last_revision_idd',
            field=models.IntegerField(null=True, verbose_name='id derni\xe8re r\xe9vision'),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='title',
            field=models.CharField(max_length=255, verbose_name='titre'),
        ),
    ]
