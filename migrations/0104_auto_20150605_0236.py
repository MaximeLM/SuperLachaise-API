# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0103_auto_20150605_0156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superlachaisecategory',
            options={'ordering': ['name', 'key'], 'verbose_name': 'superlachaise category', 'verbose_name_plural': 'superlachaise categories'},
        ),
    ]
