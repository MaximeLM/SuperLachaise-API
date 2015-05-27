# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0009_auto_20150527_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperLachaiseObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
            ],
            options={
                'verbose_name': 'superlachaise object',
                'verbose_name_plural': 'superlachaise objects',
            },
        ),
        migrations.AlterModelOptions(
            name='openstreetmapelement',
            options={'verbose_name': 'openstreetmap element', 'verbose_name_plural': 'openstreetmap elements'},
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikidataLocalizedEntry', 'entr\xe9e wikidata localis\xe9e')]),
        ),
        migrations.AddField(
            model_name='superlachaiseobject',
            name='openStreetMap_element',
            field=models.ForeignKey(verbose_name='openstreetmap element', to='superlachaise_api.OpenStreetMapElement', unique=True),
        ),
    ]
