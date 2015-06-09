# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0002_auto_20150605_2112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superlachaisecategoryrelation',
            options={'ordering': ['superlachaise_poi', 'category'], 'verbose_name': 'relation superlachaisepoi-superlachaisecategory', 'verbose_name_plural': 'relations superlachaisepoi-superlachaisecategory'},
        ),
        migrations.RemoveField(
            model_name='wikimediacommonscategory',
            name='files',
        ),
        migrations.AlterField(
            model_name='superlachaisecategoryrelation',
            name='category',
            field=models.ForeignKey(verbose_name='cat\xe9gorie', to='superlachaise_api.SuperLachaiseCategory'),
        ),
    ]
