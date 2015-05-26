# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, os
from django.db import models, migrations
from django.core import serializers

def load_settings(apps, schema_editor):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../fixtures/settings.json') as data_file:    
        for obj in serializers.deserialize("json", data_file):
            obj.save()

def load_languages(apps, schema_editor):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../fixtures/languages.json') as data_file:    
        for obj in serializers.deserialize("json", data_file):
            obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0007_auto_20150526_1712'),
    ]

    operations = [
        migrations.RunPython(load_settings),
        migrations.RunPython(load_languages),
    ]
