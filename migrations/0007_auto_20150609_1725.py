# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0006_auto_20150609_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikipediapage',
            name='id',
            field=models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True),
        ),
    ]
