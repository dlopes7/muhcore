# -*- coding: utf-8 -*-

import os

os.environ['PYTHONPATH'] = '/home/david/Documents/projeto/muhcore'
os.environ['DJANGO_SETTINGS_MODULE'] = 'muhcore.settings'


import codecs
import urllib
import sys
import battlenet
import operator
import logging
import django

from collections import Counter

from battlenet import Connection, Character, Guild
from muh_core_app.models import Personagem, Guilda

django.setup()

logging.basicConfig(filename='logs/processo.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

connection = battlenet.Connection(public_key='nm3jrgp8avwjpqnptby38z763t9afyes', private_key='Edt6pnruq8ntrE4YnwnBX4ckBnMddbf8', locale='en')

nome_guilda = 'Paragon'
nome_realm = 'Lightnings Blade'
nome_battlegroup = battlenet.EUROPE

logging.debug("Guilda: " + nome_guilda + ", Realm: " + nome_realm + " BG: " + str(nome_battlegroup))

logging.debug("Conectando a battlenet")
guild = connection.get_guild(nome_battlegroup, nome_realm, nome_guilda, fields=[Guild.MEMBERS])
logging.debug("Conectado!")


guilda, created = Guilda.objects.get_or_create(nome = str(guild.name),
                                               reino = str(guild.realm),
                                               identificador = str(guild.name) + "@" + str(guild.realm)) 

if not created:
  guilda.save()

logging.debug("Guilda: " + str(guilda) + " inserida no banco de dados")

aux = 0
for member in guild.members:
  
  
  if member['character'].level == 100:
    aux+=1
    print member['character'].name, ", ", member['character'].level
    membro_all = connection.get_character(nome_battlegroup, nome_realm, member['character'].name, fields=[Character.ITEMS, Character.TALENTS])

    membro, created = Personagem.objects.get_or_create(nome = member['character'].name,
                          ilvl_equipado = int(membro_all.equipment.average_item_level_equipped),
                          guilda = guilda,
                          identificador = str(member['character'].name) + "@" + str(guild.name))
    if not created:
      membro.ilvl_equipado = int(membro_all.equipment.average_item_level_equipped)
      membro.guilda = guilda
      membro.identificador = str(member['character'].name) + "@" + str(guild.name)
      membro.save()
    else:
      membro.save()


  if aux == 5:
    break




