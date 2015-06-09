# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0003_auto_20150609_0219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='superlachaisepoi',
            name='categories',
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='superlachaise_categories',
            field=models.ManyToManyField(related_name='members', verbose_name='cat\xe9gories SuperLachaise', to='superlachaise_api.SuperLachaiseCategory', through='superlachaise_api.SuperLachaiseCategoryRelation', blank=True),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='main_image',
            field=models.ForeignKey(related_name='superlachaise_pois', on_delete=django.db.models.deletion.SET_NULL, verbose_name='image principale', blank=True, to='superlachaise_api.WikimediaCommonsFile', null=True),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='wikimedia_commons_category',
            field=models.ForeignKey(related_name='superlachaise_pois', on_delete=django.db.models.deletion.SET_NULL, verbose_name='cat\xe9gorie wikimedia commons', blank=True, to='superlachaise_api.WikimediaCommonsCategory', null=True),
        ),
    ]
