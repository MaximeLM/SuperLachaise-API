# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-31 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0024_auto_20160603_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='url_1024px',
            field=models.TextField(blank=True, verbose_name='url 1024px'),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='url_2048px',
            field=models.TextField(blank=True, verbose_name='url 2048px'),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='url_512px',
            field=models.TextField(blank=True, verbose_name='url 512px'),
        ),
    ]
