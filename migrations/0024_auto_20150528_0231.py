# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0023_remove_language_default_for_display'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wikidatalocalizedentry',
            old_name='wikidata_entry',
            new_name='parent',
        ),
        migrations.AlterUniqueTogether(
            name='wikidatalocalizedentry',
            unique_together=set([('parent', 'language')]),
        ),
    ]
