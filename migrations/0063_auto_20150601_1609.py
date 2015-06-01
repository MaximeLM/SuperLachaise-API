# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0062_auto_20150601_1557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikimediacommonsfile',
            options={'ordering': ['id'], 'verbose_name': 'fichier wikimedia commons', 'verbose_name_plural': 'fichiers wikimedia commons'},
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_class',
            field=models.CharField(max_length=255, verbose_name="classe de l'objet cible", choices=[(b'OpenStreetMapElement', '\xe9l\xe9ment OpenStreetMap'), (b'WikidataEntry', 'entr\xe9e wikidata'), (b'WikidataLocalizedEntry', 'entr\xe9e wikidata localis\xe9e'), (b'WikipediaPage', 'page wikip\xe9dia'), (b'WikimediaCommonsCategory', 'cat\xe9gorie wikimedia commons'), (b'WikimediaCommonsFile', 'fichier wikimedia commons')]),
        ),
    ]
