# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0043_auto_20150530_1836'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admincommanderror',
            options={'ordering': ['admin_command', 'type', 'target_object_class', 'target_object_id'], 'verbose_name': 'erreur commande admin', 'verbose_name_plural': 'erreurs commandes admin'},
        ),
        migrations.AddField(
            model_name='admincommand',
            name='dependency_order',
            field=models.IntegerField(null=True, verbose_name='dependency order'),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='wikidata_combined',
            field=models.CharField(max_length=255, verbose_name='wikidata combin\xe9', blank=True),
        ),
    ]
