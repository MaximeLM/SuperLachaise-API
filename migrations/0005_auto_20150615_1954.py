# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0004_auto_20150615_1948'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superlachaisecategoryrelation',
            options={'ordering': ['superlachaise_poi', 'superlachaise_category'], 'verbose_name': 'superlachaisepoi-superlachaisecategory relationship', 'verbose_name_plural': 'superlachaisepoi-superlachaisecategory relationships'},
        ),
        migrations.AddField(
            model_name='superlachaisecategoryrelation',
            name='superlachaise_category',
            field=models.ForeignKey(default=0, verbose_name='superlachaise category', to='superlachaise_api.SuperLachaiseCategory'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='superlachaisecategoryrelation',
            unique_together=set([('superlachaise_poi', 'superlachaise_category')]),
        ),
        migrations.RemoveField(
            model_name='superlachaisecategoryrelation',
            name='category',
        ),
    ]
