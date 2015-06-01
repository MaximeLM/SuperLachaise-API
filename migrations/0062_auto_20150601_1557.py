# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0061_auto_20150531_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikimediaCommonsFile',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('url', models.CharField(max_length=255, verbose_name='url')),
                ('attribution', models.CharField(max_length=255, verbose_name='attribution')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'wikimedia commons file',
                'verbose_name_plural': 'wikimedia commons files',
            },
        ),
        migrations.AlterModelOptions(
            name='wikimediacommonscategory',
            options={'ordering': ['id'], 'verbose_name': 'cat\xe9gorie wikimedia commons', 'verbose_name_plural': 'cat\xe9gories wikimedia commons'},
        ),
        migrations.RemoveField(
            model_name='wikipediapage',
            name='last_revision_id',
        ),
        migrations.AlterField(
            model_name='wikimediacommonscategory',
            name='files',
            field=models.TextField(verbose_name='fichiers', blank=True),
        ),
    ]
