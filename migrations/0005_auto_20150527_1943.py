# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0004_auto_20150527_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikiEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('wikidata', models.CharField(unique=True, max_length=255, verbose_name='wikidata')),
                ('type', models.CharField(max_length=255, verbose_name='type', choices=[(b'place', 'place'), (b'person', 'person'), (b'artist', 'artist'), (b'subject', 'subject')])),
                ('wikimedia_commons', models.CharField(max_length=255, verbose_name='wikimedia commons', blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('date_of_death', models.DateField(null=True, blank=True)),
                ('date_of_birth_accuracy', models.CharField(default=b'D', max_length=1, choices=[(b'Y', 'Year'), (b'M', 'Month'), (b'D', 'Day')])),
                ('date_of_death_accuracy', models.CharField(default=b'D', max_length=1, choices=[(b'Y', 'Year'), (b'M', 'Month'), (b'D', 'Day')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='sorting_name',
            field=models.CharField(max_length=255, verbose_name='nom pour tri', blank=True),
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
        migrations.AddField(
            model_name='wikientry',
            name='openStreetMap_element',
            field=models.ForeignKey(to='superlachaise_api.OpenStreetMapElement'),
        ),
    ]
