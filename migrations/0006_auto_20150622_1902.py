# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0005_auto_20150622_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('target_object_class', models.CharField(max_length=255, verbose_name='target object class', choices=[(b'SuperLachaiseCategory', 'superlachaise category'), (b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikimediaCommonsCategory', 'wikimedia commons category'), (b'SuperLachaisePOI', 'superlachaise POI')])),
                ('target_object_id', models.CharField(max_length=255, verbose_name='target object id')),
            ],
            options={
                'ordering': ['modified'],
                'verbose_name': 'deleted object',
                'verbose_name_plural': 'deleted objects',
            },
        ),
        migrations.AlterUniqueTogether(
            name='deletedobject',
            unique_together=set([('target_object_class', 'target_object_id')]),
        ),
    ]
