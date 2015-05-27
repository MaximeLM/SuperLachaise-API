# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0013_auto_20150527_2043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openstreetmapelement',
            options={'verbose_name': '\xe9l\xe9ment OpenStreetMap', 'verbose_name_plural': '\xe9l\xe9ments OpenStreetMap'},
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikidataLocalizedEntry', 'entr\xe9e wikidata localis\xe9e')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth_accuracy',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death_accuracy',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
        ),
    ]
