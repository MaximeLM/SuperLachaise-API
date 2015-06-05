# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0005_auto_20150605_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='enumeration_last_separator',
        ),
        migrations.AddField(
            model_name='language',
            name='last_enumeration_separator',
            field=models.CharField(default='bj', max_length=255, verbose_name='last enumeration separator'),
            preserve_default=False,
        ),
    ]
