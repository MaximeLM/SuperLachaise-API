# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='categories',
            field=models.ManyToManyField(related_name='members', verbose_name='cat\xe9gorie', to='superlachaise_api.SuperLachaiseCategory', through='superlachaise_api.SuperLachaiseCategoryRelation', blank=True),
        ),
    ]
