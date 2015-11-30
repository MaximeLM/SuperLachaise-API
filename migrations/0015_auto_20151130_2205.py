# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0014_auto_20151129_1815'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dbversion',
            options={'ordering': ['-version_id'], 'verbose_name': 'DB version', 'verbose_name_plural': 'DB versions'},
        ),
    ]
