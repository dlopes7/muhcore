# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0003_auto_20150114_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField(auto_now=True)),
                ('ilvl_equipado', models.IntegerField()),
                ('personagem', models.ForeignKey(blank=True, to='muh_core_app.Personagem', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
