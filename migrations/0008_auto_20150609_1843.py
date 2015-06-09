# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0007_auto_20150609_1725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikipediapage',
            options={'ordering': ['wikidata_localized_entry'], 'verbose_name': 'page wikip\xe9dia', 'verbose_name_plural': 'pages wikip\xe9dia'},
        ),
        migrations.RemoveField(
            model_name='wikidatalocalizedentry',
            name='intro',
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikipediaPage', 'page wikip\xe9dia'), (b'WikimediaCommonsCategory', 'cat\xe9gorie wikimedia commons'), (b'WikimediaCommonsFile', 'fichier wikimedia commons'), (b'SuperLachaisePOI', 'POI SuperLachaise')]),
        ),
    ]
