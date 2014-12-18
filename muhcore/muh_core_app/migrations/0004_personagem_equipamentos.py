# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0003_equipamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='personagem',
            name='equipamentos',
            field=models.ManyToManyField(to='muh_core_app.Equipamento'),
            preserve_default=True,
        ),
    ]
