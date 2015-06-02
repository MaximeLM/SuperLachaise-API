# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0086_wikidatalocalizedentry_intro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikipediapage',
            name='wikidata_localized_entry',
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name='target object class', choices=[(b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikimediaCommonsCategory', 'wikimedia commons category'), (b'WikimediaCommonsFile', 'wikimedia commons file')]),
        ),
        migrations.DeleteModel(
            name='WikipediaPage',
        ),
    ]
