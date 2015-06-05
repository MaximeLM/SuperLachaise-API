# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0003_language_enumeration_last_separator'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='enumeration_separator',
            field=models.CharField(max_length=255, verbose_name='enumeration separator', blank=True),
        ),
    ]
