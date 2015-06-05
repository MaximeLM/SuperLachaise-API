# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0105_auto_20150605_1059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superlachaisecategory',
            options={'ordering': ['key', 'name'], 'verbose_name': 'superlachaise category', 'verbose_name_plural': 'superlachaise categories'},
        ),
        migrations.AlterUniqueTogether(
            name='superlachaisecategory',
            unique_together=set([('key', 'name')]),
        ),
    ]
