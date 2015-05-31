# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0050_auto_20150531_0055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikipediapage',
            options={'ordering': ['title', 'language'], 'verbose_name': 'page wikip\xe9dia', 'verbose_name_plural': 'pages wikip\xe9dia'},
        ),
        migrations.AddField(
            model_name='wikipediapage',
            name='title',
            field=models.CharField(default='', max_length=255, verbose_name='title'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='wikipediapage',
            unique_together=set([('language', 'title')]),
        ),
        migrations.RemoveField(
            model_name='wikipediapage',
            name='name',
        ),
    ]
