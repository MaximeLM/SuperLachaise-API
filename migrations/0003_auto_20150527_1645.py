# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0002_auto_20150527_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admincommand',
            options={'verbose_name': 'commande admin', 'verbose_name_plural': 'commandes admin'},
        ),
        migrations.AlterModelOptions(
            name='openstreetmapelement',
            options={'verbose_name': '\xe9l\xe9ment OpenStreetMap', 'verbose_name_plural': '\xe9l\xe9ments OpenStreetMap'},
        ),
        migrations.AlterModelOptions(
            name='pendingmodification',
            options={'verbose_name': 'modification en attente', 'verbose_name_plural': 'modifications en attente'},
        ),
        migrations.AlterModelOptions(
            name='setting',
            options={'verbose_name': 'pr\xe9f\xe9rence', 'verbose_name_plural': 'pr\xe9f\xe9rences'},
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='historic',
            field=models.CharField(max_length=255, verbose_name='historic', blank=True),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='id',
            field=models.BigIntegerField(serialize=False, verbose_name='id', primary_key=True),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='latitude',
            field=models.DecimalField(verbose_name='latitude', max_digits=10, decimal_places=7),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='longitude',
            field=models.DecimalField(verbose_name='longitude', max_digits=10, decimal_places=7),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nom'),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='type',
            field=models.CharField(max_length=255, verbose_name='type', choices=[(b'node', 'noeud'), (b'way', 'chemin'), (b'relation', 'relation')]),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='wikidata',
            field=models.CharField(max_length=255, verbose_name='wikidata', blank=True),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='wikimedia_commons',
            field=models.CharField(max_length=255, verbose_name='wikimedia commons', blank=True),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='wikipedia',
            field=models.CharField(max_length=255, verbose_name='wikip\xe9dia', blank=True),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='action',
            field=models.CharField(max_length=255, verbose_name='action', choices=[(b'create', 'cr\xe9er'), (b'modify', 'modifier'), (b'delete', 'supprimer')]),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='modified_fields',
            field=models.TextField(verbose_name='champs modifi\xe9s', blank=True),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap')]),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_id',
            field=models.BigIntegerField(verbose_name="id de l'objet cible"),
        ),
        migrations.AlterField(
            model_name='setting',
            name='category',
            field=models.CharField(max_length=255, verbose_name='cat\xe9gorie'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='key',
            field=models.CharField(max_length=255, verbose_name='cl\xe9'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='value',
            field=models.CharField(max_length=255, verbose_name='valeur', blank=True),
        ),
    ]
