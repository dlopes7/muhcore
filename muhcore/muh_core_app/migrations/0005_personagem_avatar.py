# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0004_auto_20141218_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='personagem',
            name='avatar',
            field=models.CharField(default=1, max_length=800),
            preserve_default=False,
        ),
    ]
