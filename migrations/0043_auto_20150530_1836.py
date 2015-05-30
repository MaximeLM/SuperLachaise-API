# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0042_auto_20150530_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='admincommanderror',
            name='target_object_class',
            field=models.CharField(blank=True, max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikidataLocalizedEntry', 'entr\xe9e wikidata localis\xe9e')]),
        ),
        migrations.AddField(
            model_name='admincommanderror',
            name='target_object_id',
            field=models.CharField(max_length=255, verbose_name="id de l'objet cible", blank=True),
        ),
    ]
