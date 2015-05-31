# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0051_auto_20150531_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikidataLocalizedEntry', 'entr\xe9e wikidata localis\xe9e'), (b'WikipediaPage', 'page wikip\xe9dia')]),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='id',
            field=models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True),
        ),
    ]
