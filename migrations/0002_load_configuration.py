# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import models, migrations

def load_configuration(apps, schema_editor):
    call_command("load_configuration")

class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_configuration),
    ]
