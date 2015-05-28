# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0025_auto_20150528_0330'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admincommand',
            options={'ordering': ['name'], 'verbose_name': 'commande admin', 'verbose_name_plural': 'commandes admin'},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ['code'], 'verbose_name': 'langage', 'verbose_name_plural': 'langages'},
        ),
        migrations.AlterModelOptions(
            name='localizedwikidataentry',
            options={'ordering': ['parent', 'language'], 'verbose_name': 'entr\xe9e wikidata localis\xe9e', 'verbose_name_plural': 'entr\xe9es wikidata localis\xe9es'},
        ),
        migrations.AlterModelOptions(
            name='openstreetmapelement',
            options={'ordering': ['sorting_name', 'name'], 'verbose_name': '\xe9l\xe9ment OpenStreetMap', 'verbose_name_plural': '\xe9l\xe9ments OpenStreetMap'},
        ),
        migrations.AlterModelOptions(
            name='pendingmodification',
            options={'ordering': ['action', 'target_object_class', 'target_object_id'], 'verbose_name': 'modification en attente', 'verbose_name_plural': 'modifications en attente'},
        ),
        migrations.AlterModelOptions(
            name='setting',
            options={'ordering': ['category', 'key'], 'verbose_name': 'param\xe8tre', 'verbose_name_plural': 'param\xe8tres'},
        ),
        migrations.AlterModelOptions(
            name='wikidataentry',
            options={'ordering': ['type', 'id'], 'verbose_name': 'entr\xe9e wikidata', 'verbose_name_plural': 'entr\xe9es wikidata'},
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='type',
            field=models.CharField(max_length=255, verbose_name='type', choices=[(b'node', b'node'), (b'way', b'way'), (b'relation', b'relation')]),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='action',
            field=models.CharField(max_length=255, verbose_name='action', choices=[(b'create', b'create'), (b'modify', b'modify'), (b'delete', b'delete')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de naissance', choices=[(b'Year', b'Year'), (b'Month', b'Month'), (b'Day', b'Day')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de d\xe9c\xe8s', choices=[(b'Year', b'Year'), (b'Month', b'Month'), (b'Day', b'Day')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='type',
            field=models.CharField(max_length=255, verbose_name='type', choices=[(b'place', b'place'), (b'person', b'person'), (b'artist', b'artist'), (b'subject', b'subject')]),
        ),
    ]
