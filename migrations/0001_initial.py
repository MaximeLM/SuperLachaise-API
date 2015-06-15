# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCommand',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, serialize=False, verbose_name='name', primary_key=True)),
                ('dependency_order', models.IntegerField(null=True, verbose_name='dependency order', blank=True)),
                ('last_executed', models.DateTimeField(null=True, verbose_name='last executed', blank=True)),
                ('last_result', models.TextField(null=True, verbose_name='last result', blank=True)),
            ],
            options={
                'ordering': ['dependency_order', 'name'],
                'verbose_name': 'admin command',
                'verbose_name_plural': 'admin commands',
            },
        ),
        migrations.CreateModel(
            name='AdminCommandError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('type', models.CharField(max_length=255, verbose_name='type', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('target_object_class', models.CharField(blank=True, max_length=255, verbose_name='target object class', choices=[(b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikidataLocalizedEntry', 'wikidata localized entry')])),
                ('target_object_id', models.CharField(max_length=255, verbose_name='target object id', blank=True)),
                ('admin_command', models.ForeignKey(verbose_name='admin command', to='superlachaise_api.AdminCommand')),
            ],
            options={
                'ordering': ['admin_command', 'type', 'target_object_class', 'target_object_id'],
                'verbose_name': 'admin command error',
                'verbose_name_plural': 'admin command errors',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('code', models.CharField(max_length=10, unique=True, serialize=False, verbose_name='code', primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('enumeration_separator', models.CharField(max_length=255, verbose_name='enumeration separator')),
                ('last_enumeration_separator', models.CharField(max_length=255, verbose_name='last enumeration separator')),
                ('artist_prefix', models.CharField(max_length=255, verbose_name='artist prefix')),
            ],
            options={
                'ordering': ['code'],
                'verbose_name': 'language',
                'verbose_name_plural': 'languages',
            },
        ),
        migrations.CreateModel(
            name='LocalizedAdminCommand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('admin_command', models.ForeignKey(related_name='localizations', verbose_name='admin command', to='superlachaise_api.AdminCommand')),
                ('language', models.ForeignKey(verbose_name='language', to='superlachaise_api.Language')),
            ],
            options={
                'ordering': ['language', 'admin_command'],
                'verbose_name': 'localized admin command',
                'verbose_name_plural': 'localized admin commands',
            },
        ),
        migrations.CreateModel(
            name='LocalizedSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('language', models.ForeignKey(verbose_name='language', to='superlachaise_api.Language')),
            ],
            options={
                'ordering': ['language', 'setting'],
                'verbose_name': 'localized setting',
                'verbose_name_plural': 'localized settings',
            },
        ),
        migrations.CreateModel(
            name='OpenStreetMapElement',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('type', models.CharField(max_length=255, verbose_name='type', choices=[(b'node', b'node'), (b'way', b'way'), (b'relation', b'relation')])),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('sorting_name', models.CharField(max_length=255, verbose_name='sorting name', blank=True)),
                ('nature', models.CharField(max_length=255, verbose_name='nature', blank=True)),
                ('latitude', models.DecimalField(verbose_name='latitude', max_digits=10, decimal_places=7)),
                ('longitude', models.DecimalField(verbose_name='longitude', max_digits=10, decimal_places=7)),
                ('wikipedia', models.CharField(max_length=255, verbose_name='wikipedia', blank=True)),
                ('wikidata', models.CharField(max_length=255, verbose_name='wikidata', blank=True)),
                ('wikidata_combined', models.CharField(max_length=255, verbose_name='wikidata combined', blank=True)),
                ('wikimedia_commons', models.CharField(max_length=255, verbose_name='wikimedia commons', blank=True)),
            ],
            options={
                'ordering': ['sorting_name', 'id'],
                'verbose_name': 'openstreetmap element',
                'verbose_name_plural': 'openstreetmap elements',
            },
        ),
        migrations.CreateModel(
            name='PendingModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('target_object_class', models.CharField(max_length=255, verbose_name='target object class', choices=[(b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikipediaPage', 'wikipedia page'), (b'WikimediaCommonsCategory', 'wikimedia commons category'), (b'WikimediaCommonsFile', 'wikimedia commons file'), (b'SuperLachaisePOI', 'superlachaise POI')])),
                ('target_object_id', models.CharField(max_length=255, verbose_name='target object id')),
                ('action', models.CharField(max_length=255, verbose_name='action', choices=[(b'create', b'create'), (b'modify', b'modify'), (b'delete', b'delete')])),
                ('modified_fields', models.TextField(verbose_name='modified fields', blank=True)),
            ],
            options={
                'ordering': ['action', 'target_object_class', 'target_object_id'],
                'verbose_name': 'pending modification',
                'verbose_name_plural': 'pending modifications',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('key', models.CharField(max_length=255, serialize=False, verbose_name='key', primary_key=True)),
                ('value', models.CharField(max_length=255, verbose_name='value', blank=True)),
            ],
            options={
                'ordering': ['key'],
                'verbose_name': 'setting',
                'verbose_name_plural': 'settings',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseCategory',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('code', models.CharField(max_length=255, unique=True, serialize=False, verbose_name='code', primary_key=True)),
                ('type', models.CharField(max_length=255, verbose_name='type')),
                ('values', models.CharField(max_length=255, verbose_name='codes', blank=True)),
            ],
            options={
                'ordering': ['type', 'code'],
                'verbose_name': 'superlachaise category',
                'verbose_name_plural': 'superlachaise categories',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseCategoryRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('category', models.ForeignKey(verbose_name='category', to='superlachaise_api.SuperLachaiseCategory')),
            ],
            options={
                'ordering': ['superlachaise_poi', 'category'],
                'verbose_name': 'superlachaisepoi-superlachaisecategory relationship',
                'verbose_name_plural': 'superlachaisepoi-superlachaisecategory relationships',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseLocalizedCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('language', models.ForeignKey(verbose_name='language', to='superlachaise_api.Language')),
                ('superlachaise_category', models.ForeignKey(related_name='localizations', verbose_name='superlachaise category', to='superlachaise_api.SuperLachaiseCategory')),
            ],
            options={
                'ordering': ['language', 'name'],
                'verbose_name': 'superlachaise localized category',
                'verbose_name_plural': 'superlachaise localized categories',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseLocalizedPOI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('sorting_name', models.CharField(max_length=255, verbose_name='sorting name', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('language', models.ForeignKey(verbose_name='language', to='superlachaise_api.Language')),
            ],
            options={
                'ordering': ['language', 'sorting_name', 'name'],
                'verbose_name': 'superlachaise localized POI',
                'verbose_name_plural': 'superlachaise localized POIs',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaisePOI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'ordering': ['openstreetmap_element'],
                'verbose_name': 'superlachaise POI',
                'verbose_name_plural': 'superlachaise POIs',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseWikidataRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('relation_type', models.CharField(max_length=255, verbose_name='relation type')),
                ('superlachaise_poi', models.ForeignKey(verbose_name='superlachaise poi', to='superlachaise_api.SuperLachaisePOI')),
            ],
            options={
                'ordering': ['superlachaise_poi', 'relation_type', 'wikidata_entry'],
                'verbose_name': 'superlachaisepoi-wikidataentry relationship',
                'verbose_name_plural': 'superlachaisepoi-wikidataentry relationships',
            },
        ),
        migrations.CreateModel(
            name='WikidataEntry',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('instance_of', models.CharField(max_length=255, verbose_name='instance of', blank=True)),
                ('sex_or_gender', models.CharField(max_length=255, verbose_name='sex or gender', blank=True)),
                ('occupations', models.CharField(max_length=255, verbose_name='occupations', blank=True)),
                ('wikimedia_commons_category', models.CharField(max_length=255, verbose_name='wikimedia commons category', blank=True)),
                ('wikimedia_commons_grave_category', models.CharField(max_length=255, verbose_name='wikimedia commons grave category', blank=True)),
                ('grave_of_wikidata', models.CharField(max_length=255, verbose_name='grave_of:wikidata', blank=True)),
                ('date_of_birth', models.DateField(null=True, verbose_name='date of birth', blank=True)),
                ('date_of_death', models.DateField(null=True, verbose_name='date of death', blank=True)),
                ('date_of_birth_accuracy', models.CharField(blank=True, max_length=255, verbose_name='date of birth accuracy', choices=[(b'Year', 'Year'), (b'Month', 'Month'), (b'Day', 'Day')])),
                ('date_of_death_accuracy', models.CharField(blank=True, max_length=255, verbose_name='date of death accuracy', choices=[(b'Year', 'Year'), (b'Month', 'Month'), (b'Day', 'Day')])),
                ('burial_plot_reference', models.CharField(max_length=255, verbose_name='burial plot reference', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'wikidata entry',
                'verbose_name_plural': 'wikidata entries',
            },
        ),
        migrations.CreateModel(
            name='WikidataLocalizedEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='name', blank=True)),
                ('wikipedia', models.CharField(max_length=255, verbose_name='wikipedia', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('language', models.ForeignKey(verbose_name='language', to='superlachaise_api.Language')),
                ('wikidata_entry', models.ForeignKey(related_name='localizations', verbose_name='wikidata entry', to='superlachaise_api.WikidataEntry')),
            ],
            options={
                'ordering': ['language', 'name'],
                'verbose_name': 'wikidata localized entry',
                'verbose_name_plural': 'wikidata localized entries',
            },
        ),
        migrations.CreateModel(
            name='WikidataOccupation',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name', blank=True)),
                ('superlachaise_category', models.ForeignKey(related_name='wikidata_occupations', verbose_name='superlachaise category', blank=True, to='superlachaise_api.SuperLachaiseCategory', null=True)),
                ('used_in', models.ManyToManyField(related_name='wikidata_occupations', verbose_name='used in', to='superlachaise_api.WikidataEntry', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'wikidata occupation',
                'verbose_name_plural': 'wikidata occupations',
            },
        ),
        migrations.CreateModel(
            name='WikimediaCommonsCategory',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('main_image', models.CharField(max_length=255, verbose_name='main image', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'wikimedia commons category',
                'verbose_name_plural': 'wikimedia commons categories',
            },
        ),
        migrations.CreateModel(
            name='WikimediaCommonsFile',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('original_url', models.CharField(max_length=500, verbose_name='original url', blank=True)),
                ('thumbnail_url', models.CharField(max_length=500, verbose_name='thumbnail url', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'wikimedia commons file',
                'verbose_name_plural': 'wikimedia commons files',
            },
        ),
        migrations.CreateModel(
            name='WikipediaPage',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('default_sort', models.CharField(max_length=255, verbose_name='default sort', blank=True)),
                ('intro', models.TextField(verbose_name='intro', blank=True)),
                ('wikidata_localized_entry', models.OneToOneField(related_name='wikipedia_page', verbose_name='wikidata localized entry', to='superlachaise_api.WikidataLocalizedEntry')),
            ],
            options={
                'ordering': ['default_sort', 'wikidata_localized_entry'],
                'verbose_name': 'wikipedia page',
                'verbose_name_plural': 'wikipedia pages',
            },
        ),
        migrations.AddField(
            model_name='superlachaisewikidatarelation',
            name='wikidata_entry',
            field=models.ForeignKey(verbose_name='wikidata entry', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='main_image',
            field=models.ForeignKey(related_name='superlachaise_pois', on_delete=django.db.models.deletion.SET_NULL, verbose_name='main image', blank=True, to='superlachaise_api.WikimediaCommonsFile', null=True),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='openstreetmap_element',
            field=models.OneToOneField(related_name='superlachaise_poi', verbose_name='openstreetmap element', to='superlachaise_api.OpenStreetMapElement'),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='superlachaise_categories',
            field=models.ManyToManyField(related_name='members', verbose_name='superlachaise categories', to='superlachaise_api.SuperLachaiseCategory', through='superlachaise_api.SuperLachaiseCategoryRelation', blank=True),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='wikidata_entries',
            field=models.ManyToManyField(related_name='superlachaise_pois', verbose_name='wikidata entries', through='superlachaise_api.SuperLachaiseWikidataRelation', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='wikimedia_commons_category',
            field=models.ForeignKey(related_name='superlachaise_pois', on_delete=django.db.models.deletion.SET_NULL, verbose_name='wikimedia commons category', blank=True, to='superlachaise_api.WikimediaCommonsCategory', null=True),
        ),
        migrations.AddField(
            model_name='superlachaiselocalizedpoi',
            name='superlachaise_poi',
            field=models.ForeignKey(related_name='localizations', verbose_name='superlachaise poi', to='superlachaise_api.SuperLachaisePOI'),
        ),
        migrations.AddField(
            model_name='superlachaisecategoryrelation',
            name='superlachaise_poi',
            field=models.ForeignKey(verbose_name='superlachaise poi', to='superlachaise_api.SuperLachaisePOI'),
        ),
        migrations.AlterUniqueTogether(
            name='pendingmodification',
            unique_together=set([('target_object_class', 'target_object_id')]),
        ),
        migrations.AddField(
            model_name='localizedsetting',
            name='setting',
            field=models.ForeignKey(related_name='localizations', verbose_name='setting', to='superlachaise_api.Setting'),
        ),
        migrations.AlterUniqueTogether(
            name='wikidatalocalizedentry',
            unique_together=set([('wikidata_entry', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='superlachaisewikidatarelation',
            unique_together=set([('superlachaise_poi', 'wikidata_entry', 'relation_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='superlachaiselocalizedpoi',
            unique_together=set([('superlachaise_poi', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='superlachaiselocalizedcategory',
            unique_together=set([('superlachaise_category', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='superlachaisecategoryrelation',
            unique_together=set([('superlachaise_poi', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='localizedsetting',
            unique_together=set([('setting', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='localizedadmincommand',
            unique_together=set([('admin_command', 'language')]),
        ),
    ]
