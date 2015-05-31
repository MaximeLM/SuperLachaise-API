# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0060_auto_20150531_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikimediaCommonsCategory',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('files', models.TextField(verbose_name='files', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'cat\xe9gorie wikimedia commons',
                'verbose_name_plural': 'wikimedia commons categories',
            },
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikidataLocalizedEntry', 'entr\xe9e wikidata localis\xe9e'), (b'WikipediaPage', 'page wikip\xe9dia'), (b'WikimediaCommonsCategory', 'cat\xe9gorie wikimedia commons')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de naissance', choices=[(b'Year', 'Ann\xe9e'), (b'Month', 'Mois'), (b'Day', 'Jour')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de d\xe9c\xe8s', choices=[(b'Year', 'Ann\xe9e'), (b'Month', 'Mois'), (b'Day', 'Jour')]),
        ),
    ]
