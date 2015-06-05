# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0100_auto_20150605_0146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superlachaiseoccupation',
            options={'ordering': ['id'], 'verbose_name': 'superlachaise occupation', 'verbose_name_plural': 'superlachaise occupations'},
        ),
    ]
