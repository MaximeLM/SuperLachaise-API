# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0058_auto_20150531_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikipediaPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('title', models.CharField(max_length=255, verbose_name='titre')),
                ('last_revision_id', models.BigIntegerField(null=True, verbose_name='id derni\xe8re r\xe9vision')),
                ('intro', models.TextField(verbose_name='intro', blank=True)),
                ('date_of_birth', models.DateField(null=True, verbose_name='date de naissance', blank=True)),
                ('date_of_death', models.DateField(null=True, verbose_name='date de d\xe9c\xe8s', blank=True)),
                ('date_of_birth_accuracy', models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de naissance', choices=[(b'Year', 'Ann\xe9e'), (b'Month', 'Mois'), (b'Day', 'Jour')])),
                ('date_of_death_accuracy', models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de d\xe9c\xe8s', choices=[(b'Year', 'Ann\xe9e'), (b'Month', 'Mois'), (b'Day', 'Jour')])),
                ('language', models.ForeignKey(verbose_name='langage', to='superlachaise_api.Language')),
            ],
            options={
                'ordering': ['title', 'language'],
                'verbose_name': 'page wikip\xe9dia',
                'verbose_name_plural': 'pages wikip\xe9dia',
            },
        ),
        migrations.AlterUniqueTogether(
            name='wikipediapage',
            unique_together=set([('language', 'title')]),
        ),
    ]
