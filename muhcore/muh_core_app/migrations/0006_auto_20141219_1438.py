# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0005_personagem_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='personagem',
            name='classe',
            field=models.CharField(default=b'1', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personagem',
            name='color',
            field=models.CharField(default=b'1', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personagem',
            name='spec',
            field=models.CharField(default=b'1', max_length=200),
            preserve_default=True,
        ),
    ]
