# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0003_auto_20141217_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='guilda',
            name='reino',
            field=models.CharField(default='none', max_length=200),
            preserve_default=False,
        ),
    ]