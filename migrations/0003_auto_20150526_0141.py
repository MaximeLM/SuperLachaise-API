# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0002_auto_20150525_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255, blank=True)),
                ('description', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='localizedopenstreetmappoi',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='localizedopenstreetmappoi',
            name='language',
        ),
        migrations.RemoveField(
            model_name='localizedopenstreetmappoi',
            name='openStreetMapPOI',
        ),
        migrations.AddField(
            model_name='openstreetmappoi',
            name='wikipedia',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='new_values',
            field=models.CharField(max_length=2000, blank=True),
        ),
        migrations.DeleteModel(
            name='LocalizedOpenStreetMapPOI',
        ),
    ]
