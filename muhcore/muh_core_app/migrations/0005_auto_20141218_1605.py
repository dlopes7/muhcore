# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muh_core_app', '0004_personagem_equipamentos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personagem',
            name='equipamentos',
        ),
        migrations.AddField(
            model_name='personagem',
            name='back',
            field=models.ForeignKey(related_name='personagem_back', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='chest',
            field=models.ForeignKey(related_name='personagem_chest', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='feet',
            field=models.ForeignKey(related_name='personagem_feet', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='finger1',
            field=models.ForeignKey(related_name='personagem_finger1', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='finger2',
            field=models.ForeignKey(related_name='personagem_finger2', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='hands',
            field=models.ForeignKey(related_name='personagem_hands', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='head',
            field=models.ForeignKey(related_name='personagem_head', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='legs',
            field=models.ForeignKey(related_name='personagem_legs', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='main_hand',
            field=models.ForeignKey(related_name='personagem_main_hand', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='off_hand',
            field=models.ForeignKey(related_name='personagem_off_hand', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='shoulder',
            field=models.ForeignKey(related_name='personagem_shoulder', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='trinket1',
            field=models.ForeignKey(related_name='personagem_trinket1', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='trinket2',
            field=models.ForeignKey(related_name='personagem_trinket2', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='waist',
            field=models.ForeignKey(related_name='personagem_waist', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personagem',
            name='wrist',
            field=models.ForeignKey(related_name='personagem_wrist', default=1, to='muh_core_app.Equipamento'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personagem',
            name='guilda',
            field=models.ForeignKey(related_name='personagem_guilda', to='muh_core_app.Guilda'),
            preserve_default=True,
        ),
    ]
