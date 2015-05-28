# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0028_auto_20150528_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='admincommand',
            name='notes',
            field=models.TextField(verbose_name='notes', blank=True),
        ),
        migrations.AddField(
            model_name='language',
            name='notes',
            field=models.TextField(verbose_name='notes', blank=True),
        ),
        migrations.AddField(
            model_name='localizedwikidataentry',
            name='notes',
            field=models.TextField(verbose_name='notes', blank=True),
        ),
        migrations.AddField(
            model_name='openstreetmapelement',
            name='notes',
            field=models.TextField(verbose_name='notes', blank=True),
        ),
        migrations.AddField(
            model_name='pendingmodification',
            name='notes',
            field=models.TextField(verbose_name='notes', blank=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='notes',
            field=models.TextField(verbose_name='notes', blank=True),
        ),
        migrations.AddField(
            model_name='wikidataentry',
            name='notes',
            field=models.TextField(verbose_name='notes', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='wikimedia_commons_category',
            field=models.CharField(max_length=255, verbose_name='cat\xe9gorie wikimedia commons', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='wikimedia_commons_grave_category',
            field=models.CharField(max_length=255, verbose_name='cat\xe9gorie tombe wikimedia commons', blank=True),
        ),
    ]
