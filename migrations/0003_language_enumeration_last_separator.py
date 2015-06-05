# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0002_remove_admincommand_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='enumeration_last_separator',
            field=models.CharField(max_length=255, verbose_name='enumeration last separator', blank=True),
        ),
    ]
