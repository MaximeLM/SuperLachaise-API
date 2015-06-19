# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name='target object class', choices=[(b'Language', 'language'), (b'Synchronization', 'synchronization'), (b'LocalizedSynchronization', 'localized synchronization'), (b'Setting', 'setting'), (b'LocalizedSetting', 'localized setting'), (b'SuperLachaiseCategory', 'superlachaise category'), (b'SuperLachaiseLocalizedCategory', 'superlachaise localized category'), (b'WikidataOccupation', 'wikidata occupation'), (b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikidataLocalizedEntry', 'wikidata localized entry'), (b'WikipediaPage', 'wikipedia page'), (b'WikimediaCommonsCategory', 'wikimedia commons category'), (b'WikimediaCommonsFile', 'wikimedia commons file'), (b'SuperLachaisePOI', 'superlachaise POI'), (b'SuperLachaiseLocalizedPOI', 'superlachaise localized POI'), (b'SuperLachaiseWikidataRelation', 'superlachaisepoi-wikidataentry relationship'), (b'SuperLachaiseCategoryRelation', 'superlachaisepoi-superlachaisecategory relationship')]),
        ),
    ]
