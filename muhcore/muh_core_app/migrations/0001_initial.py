# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guilda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
                ('reino', models.CharField(max_length=200)),
                ('identificador', models.CharField(unique=True, max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Personagem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
                ('ilvl_equipado', models.IntegerField()),
                ('identificador', models.CharField(unique=True, max_length=200)),
                ('guilda', models.ForeignKey(to='muh_core_app.Guilda')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
