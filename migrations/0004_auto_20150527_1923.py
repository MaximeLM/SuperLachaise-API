# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0003_auto_20150527_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='openstreetmapelement',
            name='sorting_name',
            field=models.CharField(max_length=255, verbose_name='sorting_name', blank=True),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='modified_fields',
            field=models.TextField(verbose_name='modified_fields', blank=True),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name='target_object_class', choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap')]),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_id',
            field=models.BigIntegerField(verbose_name='target_object_id'),
        ),
    ]
