# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guilda',
            name='identificador',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personagem',
            name='identificador',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
