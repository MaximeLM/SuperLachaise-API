# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0005_wikipediapage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admincommand',
            name='last_executed',
            field=models.DateTimeField(null=True, verbose_name='derni\xe8re ex\xe9cution', blank=True),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikipediaPage', 'wikipedia page'), (b'WikimediaCommonsCategory', 'cat\xe9gorie wikimedia commons'), (b'WikimediaCommonsFile', 'fichier wikimedia commons'), (b'SuperLachaisePOI', 'POI SuperLachaise')]),
        ),
    ]
