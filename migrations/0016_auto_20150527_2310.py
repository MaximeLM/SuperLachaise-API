# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0015_auto_20150527_2051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='setting',
            options={'verbose_name': 'param\xe8tre', 'verbose_name_plural': 'param\xe8tres'},
        ),
        migrations.RemoveField(
            model_name='wikidataentry',
            name='wikidata',
        ),
        migrations.RemoveField(
            model_name='wikidatalocalizedentry',
            name='wikipedia_intro',
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='id',
            field=models.CharField(max_length=255, serialize=False, verbose_name='wikidata', primary_key=True),
        ),
    ]
