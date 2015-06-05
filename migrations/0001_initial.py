# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCommand',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('name', models.CharField(max_length=255, serialize=False, verbose_name='nom', primary_key=True)),
                ('dependency_order', models.IntegerField(null=True, verbose_name='ordre de d\xe9pendance')),
                ('last_executed', models.DateTimeField(null=True, verbose_name='derni\xe8re ex\xe9cution')),
                ('last_result', models.TextField(null=True, verbose_name='dernier r\xe9sultat', blank=True)),
            ],
            options={
                'ordering': ['dependency_order', 'name'],
                'verbose_name': 'commande admin',
                'verbose_name_plural': 'commandes admin',
            },
        ),
        migrations.CreateModel(
            name='AdminCommandError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('type', models.CharField(max_length=255, verbose_name='type', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('target_object_class', models.CharField(blank=True, max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikidataLocalizedEntry', 'entr\xe9e wikidata localis\xe9e')])),
                ('target_object_id', models.CharField(max_length=255, verbose_name="id de l'objet cible", blank=True)),
                ('admin_command', models.ForeignKey(verbose_name='commande admin', to='superlachaise_api.AdminCommand')),
            ],
            options={
                'ordering': ['admin_command', 'type', 'target_object_class', 'target_object_id'],
                'verbose_name': 'erreur commande admin',
                'verbose_name_plural': 'erreurs commandes admin',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('code', models.CharField(max_length=10, unique=True, serialize=False, verbose_name='code', primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('enumeration_separator', models.CharField(max_length=255, verbose_name="s\xe9p\xe9rateur d'\xe9num\xe9ration")),
                ('last_enumeration_separator', models.CharField(max_length=255, verbose_name="dernier s\xe9parateur d'\xe9num\xe9ration")),
                ('artist_prefix', models.CharField(max_length=255, verbose_name='pr\xe9fixe artiste')),
            ],
            options={
                'ordering': ['code'],
                'verbose_name': 'langage',
                'verbose_name_plural': 'langages',
            },
        ),
        migrations.CreateModel(
            name='OpenStreetMapElement',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('type', models.CharField(max_length=255, verbose_name='type', choices=[(b'node', b'node'), (b'way', b'way'), (b'relation', b'relation')])),
                ('name', models.CharField(max_length=255, verbose_name='nom')),
                ('sorting_name', models.CharField(max_length=255, verbose_name='nom pour tri', blank=True)),
                ('nature', models.CharField(max_length=255, verbose_name='nature', blank=True)),
                ('latitude', models.DecimalField(verbose_name='latitude', max_digits=10, decimal_places=7)),
                ('longitude', models.DecimalField(verbose_name='longitude', max_digits=10, decimal_places=7)),
                ('wikipedia', models.CharField(max_length=255, verbose_name='wikip\xe9dia', blank=True)),
                ('wikidata', models.CharField(max_length=255, verbose_name='wikidata', blank=True)),
                ('wikidata_combined', models.CharField(max_length=255, verbose_name='wikidata combin\xe9', blank=True)),
                ('wikimedia_commons', models.CharField(max_length=255, verbose_name='wikimedia commons', blank=True)),
            ],
            options={
                'ordering': ['sorting_name', 'id'],
                'verbose_name': '\xe9l\xe9ment OpenStreetMap',
                'verbose_name_plural': '\xe9l\xe9ments OpenStreetMap',
            },
        ),
        migrations.CreateModel(
            name='PendingModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('target_object_class', models.CharField(max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikimediaCommonsCategory', 'cat\xe9gorie wikimedia commons'), (b'WikimediaCommonsFile', 'fichier wikimedia commons'), (b'SuperLachaisePOI', 'POI SuperLachaise')])),
                ('target_object_id', models.CharField(max_length=255, verbose_name="id de l'objet cible")),
                ('action', models.CharField(max_length=255, verbose_name='action', choices=[(b'create', b'create'), (b'modify', b'modify'), (b'delete', b'delete')])),
                ('modified_fields', models.TextField(verbose_name='champs modifi\xe9s', blank=True)),
            ],
            options={
                'ordering': ['action', 'target_object_class', 'target_object_id'],
                'verbose_name': 'modification en attente',
                'verbose_name_plural': 'modifications en attente',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('key', models.CharField(max_length=255, serialize=False, verbose_name='cl\xe9', primary_key=True)),
                ('value', models.CharField(max_length=255, verbose_name='valeur', blank=True)),
            ],
            options={
                'ordering': ['key'],
                'verbose_name': 'param\xe8tre',
                'verbose_name_plural': 'param\xe8tres',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseCategory',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('code', models.CharField(max_length=255, unique=True, serialize=False, verbose_name='code', primary_key=True)),
                ('type', models.CharField(max_length=255, verbose_name='type')),
                ('values', models.CharField(max_length=255, verbose_name='codes', blank=True)),
            ],
            options={
                'ordering': ['type', 'code'],
                'verbose_name': 'cat\xe9gorie SuperLachaise',
                'verbose_name_plural': 'cat\xe9gories SuperLachaise',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseCategoryRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
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
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('name', models.CharField(max_length=255, verbose_name='nom')),
                ('language', models.ForeignKey(verbose_name='langage', to='superlachaise_api.Language')),
                ('superlachaise_category', models.ForeignKey(related_name='localizations', verbose_name='cat\xe9gorie SuperLachaise', to='superlachaise_api.SuperLachaiseCategory')),
            ],
            options={
                'ordering': ['language', 'name'],
                'verbose_name': 'cat\xe9gorie SuperLachaise localis\xe9e',
                'verbose_name_plural': 'cat\xe9gories SuperLachaise localis\xe9es',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseLocalizedPOI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('name', models.CharField(max_length=255, verbose_name='nom')),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('language', models.ForeignKey(verbose_name='langage', to='superlachaise_api.Language')),
            ],
            options={
                'ordering': ['language', 'name'],
                'verbose_name': 'POI SuperLachaise localis\xe9',
                'verbose_name_plural': 'POIs SuperLachaise localis\xe9s',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseOccupation',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='nom', blank=True)),
                ('superlachaise_category', models.ForeignKey(related_name='occupations', verbose_name='cat\xe9gorie SuperLachaise', blank=True, to='superlachaise_api.SuperLachaiseCategory', null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'occupation superlachaise',
                'verbose_name_plural': 'occupations superlachaise',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaisePOI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('categories', models.ManyToManyField(related_name='superlachaise_pois', verbose_name='cat\xe9gorie', to='superlachaise_api.SuperLachaiseCategory', through='superlachaise_api.SuperLachaiseCategoryRelation', blank=True)),
            ],
            options={
                'ordering': ['openstreetmap_element'],
                'verbose_name': 'POI SuperLachaise',
                'verbose_name_plural': 'POIs SuperLachaise',
            },
        ),
        migrations.CreateModel(
            name='SuperLachaiseWikidataRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('relation_type', models.CharField(max_length=255, verbose_name='type de relation')),
                ('superlachaise_poi', models.ForeignKey(verbose_name='poi SuperLachaise', to='superlachaise_api.SuperLachaisePOI')),
            ],
            options={
                'ordering': ['superlachaise_poi', 'relation_type', 'wikidata_entry'],
                'verbose_name': 'relation superlachaisepoi-wikidataentry',
                'verbose_name_plural': 'relations superlachaisepoi-wikidataentry',
            },
        ),
        migrations.CreateModel(
            name='WikidataEntry',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('instance_of', models.CharField(max_length=255, verbose_name='nature', blank=True)),
                ('sex_or_gender', models.CharField(max_length=255, verbose_name='sexe ou genre', blank=True)),
                ('occupations', models.CharField(max_length=255, verbose_name='occupations', blank=True)),
                ('wikimedia_commons_category', models.CharField(max_length=255, verbose_name='cat\xe9gorie wikimedia commons', blank=True)),
                ('wikimedia_commons_grave_category', models.CharField(max_length=255, verbose_name='cat\xe9gorie tombe wikimedia commons', blank=True)),
                ('grave_of_wikidata', models.CharField(max_length=255, verbose_name='grave_of:wikidata', blank=True)),
                ('date_of_birth', models.DateField(null=True, verbose_name='date de naissance', blank=True)),
                ('date_of_death', models.DateField(null=True, verbose_name='date de d\xe9c\xe8s', blank=True)),
                ('date_of_birth_accuracy', models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de naissance', choices=[(b'Year', 'Ann\xe9e'), (b'Month', 'Mois'), (b'Day', 'Jour')])),
                ('date_of_death_accuracy', models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de d\xe9c\xe8s', choices=[(b'Year', 'Ann\xe9e'), (b'Month', 'Mois'), (b'Day', 'Jour')])),
                ('burial_plot_reference', models.CharField(max_length=255, verbose_name='num\xe9ro de division', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'entr\xe9e wikidata',
                'verbose_name_plural': 'entr\xe9es wikidata',
            },
        ),
        migrations.CreateModel(
            name='WikidataLocalizedEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('name', models.CharField(max_length=255, verbose_name='nom', blank=True)),
                ('wikipedia', models.CharField(max_length=255, verbose_name='wikip\xe9dia', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('intro', models.TextField(verbose_name='intro', blank=True)),
                ('language', models.ForeignKey(verbose_name='langage', to='superlachaise_api.Language')),
                ('wikidata_entry', models.ForeignKey(related_name='localizations', verbose_name='entr\xe9e wikidata', to='superlachaise_api.WikidataEntry')),
            ],
            options={
                'ordering': ['language', 'name'],
                'verbose_name': 'entr\xe9e wikidata localis\xe9e',
                'verbose_name_plural': 'entr\xe9es wikidata localis\xe9es',
            },
        ),
        migrations.CreateModel(
            name='WikimediaCommonsCategory',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('files', models.TextField(verbose_name='fichiers', blank=True)),
                ('main_image', models.CharField(max_length=255, verbose_name='image principale', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'cat\xe9gorie wikimedia commons',
                'verbose_name_plural': 'cat\xe9gories wikimedia commons',
            },
        ),
        migrations.CreateModel(
            name='WikimediaCommonsFile',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('original_url', models.CharField(max_length=500, verbose_name='url original', blank=True)),
                ('thumbnail_url', models.CharField(max_length=500, verbose_name='url vignette', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'fichier wikimedia commons',
                'verbose_name_plural': 'fichiers wikimedia commons',
            },
        ),
        migrations.AddField(
            model_name='superlachaisewikidatarelation',
            name='wikidata_entry',
            field=models.ForeignKey(verbose_name='entr\xe9e wikidata', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='main_image',
            field=models.ForeignKey(related_name='superlachaise_pois', verbose_name='image principale', blank=True, to='superlachaise_api.WikimediaCommonsFile', null=True),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='openstreetmap_element',
            field=models.OneToOneField(related_name='superlachaise_poi', verbose_name='\xe9l\xe9ment OpenStreetMap', to='superlachaise_api.OpenStreetMapElement'),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='wikidata_entries',
            field=models.ManyToManyField(related_name='superlachaise_pois', verbose_name='entr\xe9es wikidata', through='superlachaise_api.SuperLachaiseWikidataRelation', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='wikimedia_commons_category',
            field=models.ForeignKey(related_name='superlachaise_pois', verbose_name='cat\xe9gorie wikimedia commons', blank=True, to='superlachaise_api.WikimediaCommonsCategory', null=True),
        ),
        migrations.AddField(
            model_name='superlachaiseoccupation',
            name='used_in',
            field=models.ManyToManyField(related_name='superlachaise_occupations', verbose_name='utilis\xe9 dans', to='superlachaise_api.WikidataEntry', blank=True),
        ),
        migrations.AddField(
            model_name='superlachaiselocalizedpoi',
            name='superlachaise_poi',
            field=models.ForeignKey(related_name='localizations', verbose_name='poi SuperLachaise', to='superlachaise_api.SuperLachaisePOI'),
        ),
        migrations.AddField(
            model_name='superlachaisecategoryrelation',
            name='superlachaise_poi',
            field=models.ForeignKey(verbose_name='poi SuperLachaise', to='superlachaise_api.SuperLachaisePOI'),
        ),
        migrations.AlterUniqueTogether(
            name='pendingmodification',
            unique_together=set([('target_object_class', 'target_object_id')]),
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
            name='superlachaisecategoryrelation',
            unique_together=set([('superlachaise_poi', 'category')]),
        ),
    ]
