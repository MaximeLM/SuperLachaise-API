# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0003_auto_20150615_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='code',
            field=models.CharField(max_length=255, unique=True, serialize=False, verbose_name='code', primary_key=True),
        ),
    ]
