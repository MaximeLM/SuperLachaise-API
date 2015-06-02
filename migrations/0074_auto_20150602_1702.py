# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0073_auto_20150602_1617'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikidataentry',
            options={'ordering': ['id'], 'verbose_name': 'wikidata entry', 'verbose_name_plural': 'wikidata entries'},
        ),
        migrations.RemoveField(
            model_name='wikidataentry',
            name='name',
        ),
    ]
