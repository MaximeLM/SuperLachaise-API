# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0007_auto_20150527_1953'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikidataentry',
            options={'verbose_name': 'entr\xe9e wikidata', 'verbose_name_plural': 'entr\xe9es wikidata'},
        ),
        migrations.AlterModelOptions(
            name='wikidatalocalizedentry',
            options={'verbose_name': 'entr\xe9e wikidata localis\xe9e', 'verbose_name_plural': 'entr\xe9es wikidata localis\xe9es'},
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth_accuracy',
            field=models.CharField(max_length=1, choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death_accuracy',
            field=models.CharField(max_length=1, choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='type',
            field=models.CharField(max_length=255, verbose_name='type', choices=[(b'place', 'lieu'), (b'person', 'personne'), (b'artist', 'artiste'), (b'subject', 'sujet')]),
        ),
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nom', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='wikipedia_intro',
            field=models.TextField(verbose_name='intro wikip\xe9dia', blank=True),
        ),
    ]
