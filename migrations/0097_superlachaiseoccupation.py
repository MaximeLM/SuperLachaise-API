# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0096_wikidataentry_occupations'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperLachaiseOccupation',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('superlachaise_category', models.ForeignKey(related_name='occupations', verbose_name='superlachaise category', to='superlachaise_api.SuperLachaiseCategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
