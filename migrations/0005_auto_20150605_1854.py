# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0004_language_enumeration_separator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='enumeration_last_separator',
            field=models.CharField(max_length=255, verbose_name='enumeration last separator'),
        ),
        migrations.AlterField(
            model_name='language',
            name='enumeration_separator',
            field=models.CharField(max_length=255, verbose_name='enumeration separator'),
        ),
    ]
