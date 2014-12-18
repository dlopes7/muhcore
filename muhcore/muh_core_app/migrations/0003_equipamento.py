# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0002_auto_20141217_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('nome', models.CharField(max_length=200)),
                ('slot', models.CharField(max_length=200)),
                ('ilvl', models.IntegerField()),
                ('identificador', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
