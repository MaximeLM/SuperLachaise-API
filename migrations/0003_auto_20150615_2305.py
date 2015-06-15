# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0002_auto_20150615_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name='target object class', choices=[(b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikidataLocalizedEntry', 'wikidata localized entry'), (b'WikipediaPage', 'wikipedia page'), (b'WikimediaCommonsCategory', 'wikimedia commons category'), (b'WikimediaCommonsFile', 'wikimedia commons file'), (b'SuperLachaisePOI', 'superlachaise POI'), (b'SuperLachaiseWikidataRelation', 'superlachaisepoi-wikidataentry relationship'), (b'SuperLachaiseCategoryRelation', 'superlachaisepoi-superlachaisecategory relationship')]),
        ),
    ]
