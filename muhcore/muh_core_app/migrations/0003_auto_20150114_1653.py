# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0002_personagem_icon_spec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipamento',
            name='wowhead_identificador',
            field=models.CharField(max_length=300),
            preserve_default=True,
        ),
    ]
