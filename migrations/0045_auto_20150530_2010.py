# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0044_auto_20150530_1949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admincommand',
            options={'ordering': ['dependency_order', 'name'], 'verbose_name': 'commande admin', 'verbose_name_plural': 'commandes admin'},
        ),
        migrations.AlterField(
            model_name='admincommand',
            name='dependency_order',
            field=models.IntegerField(null=True, verbose_name='ordre de d\xe9pendance'),
        ),
        migrations.AlterField(
            model_name='admincommanderror',
            name='admin_command',
            field=models.ForeignKey(verbose_name='commande admin', to='superlachaise_api.AdminCommand'),
        ),
        migrations.AlterField(
            model_name='admincommanderror',
            name='type',
            field=models.CharField(max_length=255, verbose_name='type', blank=True),
        ),
        migrations.AlterField(
            model_name='localizedwikidataentry',
            name='language',
            field=models.ForeignKey(verbose_name='langage', to='superlachaise_api.Language'),
        ),
        migrations.AlterField(
            model_name='localizedwikidataentry',
            name='parent',
            field=models.ForeignKey(verbose_name='entr\xe9e wikidata', to='superlachaise_api.WikidataEntry'),
        ),
    ]
