# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0002_auto_20141217_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guilda',
            old_name='name',
            new_name='nome',
        ),
        migrations.RenameField(
            model_name='personagem',
            old_name='guild',
            new_name='guilda',
        ),
        migrations.RenameField(
            model_name='personagem',
            old_name='equipped_ilvl',
            new_name='ilvl_equipado',
        ),
        migrations.RenameField(
            model_name='personagem',
            old_name='name',
            new_name='nome',
        ),
    ]
