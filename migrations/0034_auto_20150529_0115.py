# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0033_auto_20150529_0039'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikidataentry',
            options={'ordering': ['id'], 'verbose_name': 'entr\xe9e wikidata', 'verbose_name_plural': 'entr\xe9es wikidata'},
        ),
        migrations.RemoveField(
            model_name='wikidataentry',
            name='type',
        ),
        migrations.AddField(
            model_name='wikidataentry',
            name='is_a_person',
            field=models.BooleanField(default=False, verbose_name='humain'),
        ),
    ]
