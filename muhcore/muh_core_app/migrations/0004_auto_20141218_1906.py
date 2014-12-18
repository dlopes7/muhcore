# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0003_auto_20141218_1904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipamento',
            old_name='wowhead_identidifcador',
            new_name='wowhead_identificador',
        ),
    ]
