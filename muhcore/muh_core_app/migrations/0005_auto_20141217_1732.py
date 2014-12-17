# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0004_guilda_reino'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guilda',
            name='id',
        ),
        migrations.AddField(
            model_name='guilda',
            name='identificador',
            field=models.CharField(default=b'None@None', max_length=200, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
