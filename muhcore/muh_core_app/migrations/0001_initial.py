# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
                ('slot', models.CharField(max_length=200)),
                ('ilvl', models.IntegerField()),
                ('bonus', models.CharField(max_length=200)),
                ('origem', models.CharField(max_length=200)),
                ('identificador', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Guilda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
                ('reino', models.CharField(max_length=200)),
                ('identificador', models.CharField(max_length=200)),
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
                ('identificador', models.CharField(max_length=200)),
                ('back', models.ForeignKey(related_name='personagem_back', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('chest', models.ForeignKey(related_name='personagem_chest', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('feet', models.ForeignKey(related_name='personagem_feet', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('finger1', models.ForeignKey(related_name='personagem_finger1', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('finger2', models.ForeignKey(related_name='personagem_finger2', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('guilda', models.ForeignKey(related_name='personagem_guilda', blank=True, to='muh_core_app.Guilda', null=True)),
                ('hands', models.ForeignKey(related_name='personagem_hands', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('head', models.ForeignKey(related_name='personagem_head', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('legs', models.ForeignKey(related_name='personagem_legs', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('main_hand', models.ForeignKey(related_name='personagem_main_hand', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('neck', models.ForeignKey(related_name='personagem_neck', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('off_hand', models.ForeignKey(related_name='personagem_off_hand', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('shoulder', models.ForeignKey(related_name='personagem_shoulder', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('trinket1', models.ForeignKey(related_name='personagem_trinket1', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('trinket2', models.ForeignKey(related_name='personagem_trinket2', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('waist', models.ForeignKey(related_name='personagem_waist', blank=True, to='muh_core_app.Equipamento', null=True)),
                ('wrist', models.ForeignKey(related_name='personagem_wrist', blank=True, to='muh_core_app.Equipamento', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
