# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0002_equipamento_wowhead_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipamento',
            name='wowhead_id',
        ),
        migrations.AddField(
            model_name='equipamento',
            name='wowhead_identidifcador',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
