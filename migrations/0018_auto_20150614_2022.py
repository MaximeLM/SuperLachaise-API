# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0017_localizedadmincommand_localizedsetting'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='localizedadmincommand',
            unique_together=set([('admin_command', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='localizedsetting',
            unique_together=set([('setting', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='superlachaiselocalizedpoi',
            unique_together=set([('superlachaise_poi', 'language')]),
        ),
    ]
