# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenStreetMapElement',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=255, choices=[(b'node', b'node'), (b'way', b'way'), (b'relation', b'relation')])),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('wikipedia', models.CharField(max_length=255, blank=True)),
                ('wikidata', models.CharField(max_length=255, blank=True)),
                ('wikimedia_commons', models.CharField(max_length=255, blank=True)),
                ('historic', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'OpenStreetMap element',
                'verbose_name_plural': 'OpenStreetMap elements',
            },
        ),
        migrations.DeleteModel(
            name='OpenStreetMapPOI',
        ),
        migrations.AlterModelOptions(
            name='admincommand',
            options={'verbose_name': 'commande administrateur', 'verbose_name_plural': 'commandes administrateur'},
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le'),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='last_executed',
            field=models.DateTimeField(null=True, verbose_name='derni\xe8re ex\xe9cution'),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='last_result',
            field=models.TextField(null=True, verbose_name='dernier r\xe9sultat', blank=True),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le'),
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='nom'),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le'),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le'),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, choices=[(b'OpenStreetMapElement', 'OpenStreetMap element')]),
        ),
        migrations.AlterField(
            model_name='setting',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le'),
        ),
    ]
