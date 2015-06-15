# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0002_load_configuration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admincommanderror',
            name='admin_command',
        ),
        migrations.DeleteModel(
            name='AdminCommandError',
        ),
    ]
