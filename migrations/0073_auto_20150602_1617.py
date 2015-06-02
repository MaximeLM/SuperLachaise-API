# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0072_auto_20150602_0553'),
    ]

    operations = [
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
            ],
            options={
                'ordering': ['name', 'language'],
                'verbose_name': 'wikidata localized entry',
                'verbose_name_plural': 'wikidata localized entries',
            },
        ),
        migrations.AlterUniqueTogether(
            name='localizedwikidataentry',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='localizedwikidataentry',
            name='language',
        ),
        migrations.RemoveField(
            model_name='localizedwikidataentry',
            name='parent',
        ),
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
            options={'ordering': ['category', 'key'], 'verbose_name': 'setting', 'verbose_name_plural': 'settings'},
        ),
        migrations.AlterModelOptions(
            name='wikidataentry',
            options={'ordering': ['name', 'id'], 'verbose_name': 'wikidata entry', 'verbose_name_plural': 'wikidata entries'},
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
            options={'ordering': ['title', 'language'], 'verbose_name': 'wikipedia page', 'verbose_name_plural': 'wikipedia pages'},
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='dependency_order',
            field=models.IntegerField(null=True, verbose_name='dependency order'),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='last_executed',
            field=models.DateTimeField(null=True, verbose_name='last executed'),
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
            field=models.CharField(unique=True, max_length=255, verbose_name='name'),
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
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='language',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
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
            field=models.CharField(max_length=255, verbose_name='target object class', choices=[(b'OpenStreetMapElement', 'openstreetmap element'), (b'WikidataEntry', 'wikidata entry'), (b'WikipediaPage', 'wikipedia page'), (b'WikimediaCommonsCategory', 'wikimedia commons category'), (b'WikimediaCommonsFile', 'wikimedia commons file')]),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_id',
            field=models.CharField(max_length=255, verbose_name='target object id'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='category',
            field=models.CharField(max_length=255, verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='key',
            field=models.CharField(max_length=255, verbose_name='key'),
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
            name='name',
            field=models.CharField(max_length=255, verbose_name='name', blank=True),
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
            model_name='wikimediacommonscategory',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='wikimediacommonscategory',
            name='files',
            field=models.TextField(verbose_name='files', blank=True),
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
            name='language',
            field=models.ForeignKey(verbose_name='language', to='superlachaise_api.Language'),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.DeleteModel(
            name='LocalizedWikidataEntry',
        ),
        migrations.AddField(
            model_name='wikidatalocalizedentry',
            name='language',
            field=models.ForeignKey(verbose_name='language', to='superlachaise_api.Language'),
        ),
        migrations.AddField(
            model_name='wikidatalocalizedentry',
            name='wikidata_entry',
            field=models.ForeignKey(verbose_name='wikidata entry', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.AlterUniqueTogether(
            name='wikidatalocalizedentry',
            unique_together=set([('wikidata_entry', 'language')]),
        ),
    ]
