# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0047_auto_20150530_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikipediaPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('name', models.CharField(max_length=255, verbose_name='nom', blank=True)),
                ('intro', models.TextField(verbose_name='intro', blank=True)),
                ('date_of_birth', models.DateField(null=True, verbose_name='date de naissance', blank=True)),
                ('date_of_death', models.DateField(null=True, verbose_name='date de d\xe9c\xe8s', blank=True)),
                ('date_of_birth_accuracy', models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de naissance', choices=[(b'Year', b'Year'), (b'Month', b'Month'), (b'Day', b'Day')])),
                ('date_of_death_accuracy', models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de d\xe9c\xe8s', choices=[(b'Year', b'Year'), (b'Month', b'Month'), (b'Day', b'Day')])),
                ('language', models.ForeignKey(verbose_name='langage', to='superlachaise_api.Language')),
            ],
            options={
                'ordering': ['name', 'language'],
                'verbose_name': 'wikipedia page',
                'verbose_name_plural': 'wikipedia pages',
            },
        ),
        migrations.AlterUniqueTogether(
            name='wikipediapage',
            unique_together=set([('language', 'name')]),
        ),
    ]
