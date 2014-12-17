# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Guild',
            new_name='Guilda',
        ),
        migrations.RenameModel(
            old_name='Character',
            new_name='Personagem',
        ),
    ]
