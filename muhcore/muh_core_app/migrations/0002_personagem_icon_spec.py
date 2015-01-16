# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='personagem',
            name='icon_spec',
            field=models.CharField(default=b'1', max_length=600),
            preserve_default=True,
        ),
    ]
