# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0077_auto_20150602_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperLachaiseCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'superlachaise category',
                'verbose_name_plural': 'superlachaise categories',
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
                'ordering': ['name', 'language'],
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
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('language', models.ForeignKey(verbose_name='language', to='superlachaise_api.Language')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'superlachaise localized POI',
                'verbose_name_plural': 'superlachaise localized POIs',
            },
        ),
        migrations.AlterModelOptions(
            name='superlachaisepoi',
            options={'ordering': ['openstreetmap_element'], 'verbose_name': 'superlachaise POI', 'verbose_name_plural': 'superlachaise POIs'},
        ),
        migrations.AddField(
            model_name='superlachaiselocalizedpoi',
            name='superlachaise_poi',
            field=models.ForeignKey(related_name='localizations', verbose_name='superlachaise poi', to='superlachaise_api.SuperLachaisePOI'),
        ),
    ]
