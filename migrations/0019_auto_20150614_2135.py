# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0018_auto_20150614_2022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admincommand',
            options={'ordering': ['dependency_order', 'name'], 'verbose_name': 'admin command', 'verbose_name_plural': 'admin commands'},
        ),
        migrations.AlterModelOptions(
            name='admincommanderror',
            options={'ordering': ['admin_command', 'type', 'target_object_class', 'target_object_id'], 'verbose_name': 'admin command error', 'verbose_name_plural': 'admin command errors'},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ['code'], 'verbose_name': 'language', 'verbose_name_plural': 'languages'},
        ),
        migrations.AlterModelOptions(
            name='openstreetmapelement',
            options={'ordering': ['sorting_name', 'id'], 'verbose_name': 'openstreetmap element', 'verbose_name_plural': 'openstreetmap elements'},
        ),
        migrations.AlterModelOptions(
            name='pendingmodification',
            options={'ordering': ['action', 'target_object_class', 'target_object_id'], 'verbose_name': 'pending modification', 'verbose_name_plural': 'pending modifications'},
        ),
        migrations.AlterModelOptions(
            name='setting',
            options={'ordering': ['key'], 'verbose_name': 'setting', 'verbose_name_plural': 'settings'},
        ),
        migrations.AlterModelOptions(
            name='superlachaisecategory',
            options={'ordering': ['type', 'code'], 'verbose_name': 'superlachaise category', 'verbose_name_plural': 'superlachaise categories'},
        ),
        migrations.AlterModelOptions(
            name='superlachaisecategoryrelation',
            options={'ordering': ['superlachaise_poi', 'category'], 'verbose_name': 'superlachaisepoi-superlachaisecategory relationship', 'verbose_name_plural': 'superlachaisepoi-superlachaisecategory relationships'},
        ),
        migrations.AlterModelOptions(
            name='superlachaiselocalizedcategory',
            options={'ordering': ['language', 'name'], 'verbose_name': 'superlachaise localized category', 'verbose_name_plural': 'superlachaise localized categories'},
        ),
        migrations.AlterModelOptions(
            name='superlachaiselocalizedpoi',
            options={'ordering': ['language', 'sorting_name', 'name'], 'verbose_name': 'superlachaise localized POI', 'verbose_name_plural': 'superlachaise localized POIs'},
        ),
        migrations.AlterModelOptions(
            name='superlachaisepoi',
            options={'ordering': ['openstreetmap_element'], 'verbose_name': 'superlachaise POI', 'verbose_name_plural': 'superlachaise POIs'},
        ),
        migrations.AlterModelOptions(
            name='superlachaisewikidatarelation',
            options={'ordering': ['superlachaise_poi', 'relation_type', 'wikidata_entry'], 'verbose_name': 'superlachaisepoi-wikidataentry relationship', 'verbose_name_plural': 'superlachaisepoi-wikidataentry relationships'},
        ),
        migrations.AlterModelOptions(
            name='wikidataentry',
            options={'ordering': ['id'], 'verbose_name': 'wikidata entry', 'verbose_name_plural': 'wikidata entries'},
        ),
        migrations.AlterModelOptions(
            name='wikidatalocalizedentry',
            options={'ordering': ['language', 'name'], 'verbose_name': 'wikidata localized entry', 'verbose_name_plural': 'wikidata localized entries'},
        ),
        migrations.AlterModelOptions(
            name='wikidataoccupation',
            options={'ordering': ['id'], 'verbose_name': 'wikidata occupation', 'verbose_name_plural': 'wikidata occupations'},
        ),
        migrations.AlterModelOptions(
            name='wikimediacommonscategory',
            options={'ordering': ['id'], 'verbose_name': 'wikimedia commons category', 'verbose_name_plural': 'wikimedia commons categories'},
        ),
        migrations.AlterModelOptions(
            name='wikimediacommonsfile',
            options={'ordering': ['id'], 'verbose_name': 'wikimedia commons file', 'verbose_name_plural': 'wikimedia commons files'},
        ),
        migrations.AlterModelOptions(
            name='wikipediapage',
            options={'ordering': ['default_sort', 'wikidata_localized_entry'], 'verbose_name': 'wikipedia page', 'verbose_name_plural': 'wikipedia pages'},
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='dependency_order',
            field=models.IntegerField(null=True, verbose_name='dependency order', blank=True),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='last_executed',
            field=models.DateTimeField(null=True, verbose_name='last executed', blank=True),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='last_result',
            field=models.TextField(null=True, verbose_name='last result', blank=True),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='name',
            field=models.CharField(max_length=255, serialize=False, verbose_name='name', primary_key=True),
        ),
        migrations.AlterField(
            model_name='admincommanderror',
            name='admin_command',
            field=models.ForeignKey(verbose_name='admin command', to='superlachaise_api.AdminCommand'),
        ),
        migrations.AlterField(
            model_name='admincommanderror',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='admincommanderror',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='admincommanderror',
            name='target_object_class',
            field=models.CharField(blank=True, max_length=255, verbose_name='target object class', choices=[(b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikidataLocalizedEntry', 'wikidata localized entry')]),
        ),
        migrations.AlterField(
            model_name='admincommanderror',
            name='target_object_id',
            field=models.CharField(max_length=255, verbose_name='target object id', blank=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='artist_prefix',
            field=models.CharField(max_length=255, verbose_name='artist prefix'),
        ),
        migrations.AlterField(
            model_name='language',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='language',
            name='enumeration_separator',
            field=models.CharField(max_length=255, verbose_name='enumeration separator'),
        ),
        migrations.AlterField(
            model_name='language',
            name='last_enumeration_separator',
            field=models.CharField(max_length=255, verbose_name='last enumeration separator'),
        ),
        migrations.AlterField(
            model_name='language',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='localizedadmincommand',
            name='admin_command',
            field=models.ForeignKey(related_name='localizations', verbose_name='admin command', to='superlachaise_api.AdminCommand'),
        ),
        migrations.AlterField(
            model_name='localizedadmincommand',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='localizedadmincommand',
            name='language',
            field=models.ForeignKey(verbose_name='language', to='superlachaise_api.Language'),
        ),
        migrations.AlterField(
            model_name='localizedadmincommand',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='localizedsetting',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='localizedsetting',
            name='language',
            field=models.ForeignKey(verbose_name='language', to='superlachaise_api.Language'),
        ),
        migrations.AlterField(
            model_name='localizedsetting',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='localizedsetting',
            name='setting',
            field=models.ForeignKey(related_name='localizations', verbose_name='setting', to='superlachaise_api.Setting'),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='sorting_name',
            field=models.CharField(max_length=255, verbose_name='sorting name', blank=True),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='wikidata_combined',
            field=models.CharField(max_length=255, verbose_name='wikidata combined', blank=True),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='wikipedia',
            field=models.CharField(max_length=255, verbose_name='wikipedia', blank=True),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='modified_fields',
            field=models.TextField(verbose_name='modified fields', blank=True),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name='target object class', choices=[(b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikipediaPage', 'wikipedia page'), (b'WikimediaCommonsCategory', 'wikimedia commons category'), (b'WikimediaCommonsFile', 'wikimedia commons file'), (b'SuperLachaisePOI', 'superlachaise POI')]),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_id',
            field=models.CharField(max_length=255, verbose_name='target object id'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='key',
            field=models.CharField(max_length=255, serialize=False, verbose_name='key', primary_key=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='value',
            field=models.CharField(max_length=255, verbose_name='value', blank=True),
        ),
        migrations.AlterField(
            model_name='superlachaisecategory',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='superlachaisecategory',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='superlachaisecategoryrelation',
            name='category',
            field=models.ForeignKey(verbose_name='category', to='superlachaise_api.SuperLachaiseCategory'),
        ),
        migrations.AlterField(
            model_name='superlachaisecategoryrelation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='superlachaisecategoryrelation',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='superlachaisecategoryrelation',
            name='superlachaise_poi',
            field=models.ForeignKey(verbose_name='superlachaise poi', to='superlachaise_api.SuperLachaisePOI'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedcategory',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedcategory',
            name='language',
            field=models.ForeignKey(verbose_name='language', to='superlachaise_api.Language'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedcategory',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedcategory',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedcategory',
            name='superlachaise_category',
            field=models.ForeignKey(related_name='localizations', verbose_name='superlachaise category', to='superlachaise_api.SuperLachaiseCategory'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedpoi',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedpoi',
            name='language',
            field=models.ForeignKey(verbose_name='language', to='superlachaise_api.Language'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedpoi',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedpoi',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedpoi',
            name='sorting_name',
            field=models.CharField(max_length=255, verbose_name='sorting name', blank=True),
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedpoi',
            name='superlachaise_poi',
            field=models.ForeignKey(related_name='localizations', verbose_name='superlachaise poi', to='superlachaise_api.SuperLachaisePOI'),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='main_image',
            field=models.ForeignKey(related_name='superlachaise_pois', on_delete=django.db.models.deletion.SET_NULL, verbose_name='main image', blank=True, to='superlachaise_api.WikimediaCommonsFile', null=True),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='openstreetmap_element',
            field=models.OneToOneField(related_name='superlachaise_poi', verbose_name='openstreetmap element', to='superlachaise_api.OpenStreetMapElement'),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='superlachaise_categories',
            field=models.ManyToManyField(related_name='members', verbose_name='superlachaise categories', to='superlachaise_api.SuperLachaiseCategory', through='superlachaise_api.SuperLachaiseCategoryRelation', blank=True),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='wikidata_entries',
            field=models.ManyToManyField(related_name='superlachaise_pois', verbose_name='wikidata entries', through='superlachaise_api.SuperLachaiseWikidataRelation', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='wikimedia_commons_category',
            field=models.ForeignKey(related_name='superlachaise_pois', on_delete=django.db.models.deletion.SET_NULL, verbose_name='wikimedia commons category', blank=True, to='superlachaise_api.WikimediaCommonsCategory', null=True),
        ),
        migrations.AlterField(
            model_name='superlachaisewikidatarelation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='superlachaisewikidatarelation',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='superlachaisewikidatarelation',
            name='relation_type',
            field=models.CharField(max_length=255, verbose_name='relation type'),
        ),
        migrations.AlterField(
            model_name='superlachaisewikidatarelation',
            name='superlachaise_poi',
            field=models.ForeignKey(verbose_name='superlachaise poi', to='superlachaise_api.SuperLachaisePOI'),
        ),
        migrations.AlterField(
            model_name='superlachaisewikidatarelation',
            name='wikidata_entry',
            field=models.ForeignKey(verbose_name='wikidata entry', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='burial_plot_reference',
            field=models.CharField(max_length=255, verbose_name='burial plot reference', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name='date of birth', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='date of birth accuracy', choices=[(b'Year', 'Year'), (b'Month', 'Month'), (b'Day', 'Day')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death',
            field=models.DateField(null=True, verbose_name='date of death', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='date of death accuracy', choices=[(b'Year', 'Year'), (b'Month', 'Month'), (b'Day', 'Day')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='instance_of',
            field=models.CharField(max_length=255, verbose_name='instance of', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='sex_or_gender',
            field=models.CharField(max_length=255, verbose_name='sex or gender', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='wikimedia_commons_category',
            field=models.CharField(max_length=255, verbose_name='wikimedia commons category', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='wikimedia_commons_grave_category',
            field=models.CharField(max_length=255, verbose_name='wikimedia commons grave category', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='language',
            field=models.ForeignKey(verbose_name='language', to='superlachaise_api.Language'),
        ),
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='wikidata_entry',
            field=models.ForeignKey(related_name='localizations', verbose_name='wikidata entry', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='wikipedia',
            field=models.CharField(max_length=255, verbose_name='wikipedia', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataoccupation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='wikidataoccupation',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='wikidataoccupation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataoccupation',
            name='superlachaise_category',
            field=models.ForeignKey(related_name='wikidata_occupations', verbose_name='superlachaise category', blank=True, to='superlachaise_api.SuperLachaiseCategory', null=True),
        ),
        migrations.AlterField(
            model_name='wikidataoccupation',
            name='used_in',
            field=models.ManyToManyField(related_name='wikidata_occupations', verbose_name='used in', to='superlachaise_api.WikidataEntry', blank=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonscategory',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='wikimediacommonscategory',
            name='main_image',
            field=models.CharField(max_length=255, verbose_name='main image', blank=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonscategory',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='original_url',
            field=models.CharField(max_length=500, verbose_name='original url', blank=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='thumbnail_url',
            field=models.CharField(max_length=500, verbose_name='thumbnail url', blank=True),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='default_sort',
            field=models.CharField(max_length=255, verbose_name='default sort', blank=True),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='wikidata_localized_entry',
            field=models.OneToOneField(related_name='wikipedia_page', verbose_name='wikidata localized entry', to='superlachaise_api.WikidataLocalizedEntry'),
        ),
    ]
