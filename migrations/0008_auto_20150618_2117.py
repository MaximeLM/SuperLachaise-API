# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0007_auto_20150616_2117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pendingmodification',
            options={'ordering': ['modified'], 'verbose_name': 'pending modification', 'verbose_name_plural': 'pending modifications'},
        ),
        migrations.RemoveField(
            model_name='admincommand',
            name='last_result',
        ),
        migrations.AddField(
            model_name='admincommand',
            name='created_objects',
            field=models.IntegerField(default=0, verbose_name='created objects'),
        ),
        migrations.AddField(
            model_name='admincommand',
            name='deleted_objects',
            field=models.IntegerField(default=0, verbose_name='deleted objects'),
        ),
        migrations.AddField(
            model_name='admincommand',
            name='errors',
            field=models.TextField(null=True, verbose_name='errors', blank=True),
        ),
        migrations.AddField(
            model_name='admincommand',
            name='modified_objects',
            field=models.IntegerField(default=0, verbose_name='modified objects'),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name='target object class', choices=[(b'Language', 'language'), (b'AdminCommand', 'admin command'), (b'LocalizedAdminCommand', 'localized admin command'), (b'Setting', 'setting'), (b'LocalizedSetting', 'localized setting'), (b'SuperLachaiseCategory', 'superlachaise category'), (b'SuperLachaiseLocalizedCategory', 'superlachaise localized category'), (b'WikidataOccupation', 'wikidata occupation'), (b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikidataLocalizedEntry', 'wikidata localized entry'), (b'WikipediaPage', 'wikipedia page'), (b'WikimediaCommonsCategory', 'wikimedia commons category'), (b'WikimediaCommonsFile', 'wikimedia commons file'), (b'SuperLachaisePOI', 'superlachaise POI'), (b'SuperLachaiseWikidataRelation', 'superlachaisepoi-wikidataentry relationship'), (b'SuperLachaiseCategoryRelation', 'superlachaisepoi-superlachaisecategory relationship')]),
        ),
        migrations.AlterField(
            model_name='superlachaisecategory',
            name='values',
            field=models.CharField(max_length=255, verbose_name='values', blank=True),
        ),
    ]
