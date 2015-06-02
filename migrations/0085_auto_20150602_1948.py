# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0084_auto_20150602_1916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikipediapage',
            options={'ordering': ['wikidata_localized_entry'], 'verbose_name': 'wikipedia page', 'verbose_name_plural': 'wikipedia pages'},
        ),
        migrations.AddField(
            model_name='wikipediapage',
            name='wikidata_localized_entry',
            field=models.OneToOneField(related_name='wikipedia_page', default=1, verbose_name='wikidata localized entry', to='superlachaise_api.WikidataLocalizedEntry'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='wikipediapage',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='wikipediapage',
            name='language',
        ),
        migrations.RemoveField(
            model_name='wikipediapage',
            name='title',
        ),
    ]
