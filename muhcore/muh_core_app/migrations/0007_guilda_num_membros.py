# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0006_auto_20141219_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='guilda',
            name='num_membros',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
