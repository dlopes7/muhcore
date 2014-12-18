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
from muh_core_app.models import Personagem, Guilda, Equipamento


def criarEquipamento(equipamento, slot):
  equip_criado, created = Equipamento.objects.get_or_create(identificador = int(equipamento.id),
                                                    defaults={'nome': equipamento.name,
                                                    'origem' : equipament.context,
                                                    'ilvl': int(equipamento.ilvl),
                                                    'slot': slot})

  equip_criado.save()
  return equip_criado


django.setup()

logging.basicConfig(filename='logs/processo.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

connection = battlenet.Connection(public_key='nm3jrgp8avwjpqnptby38z763t9afyes', private_key='Edt6pnruq8ntrE4YnwnBX4ckBnMddbf8', locale='en')

nome_guilda = 'EvecraideR Gaming'
nome_realm = 'Nemesis'
nome_battlegroup = battlenet.UNITED_STATES

logging.debug("Guilda: " + nome_guilda + ", Realm: " + nome_realm + " BG: " + str(nome_battlegroup))

logging.debug("Conectando a battlenet")
guild = connection.get_guild(nome_battlegroup, nome_realm, nome_guilda, fields=[Guild.MEMBERS])
logging.debug("Conectado!")


guilda, created = Guilda.objects.get_or_create(nome = str(guild.name),
                                               reino = str(guild.realm),
                                               identificador = str(guild.name) + "@" + str(guild.realm)) 

if not created:
  guilda.save()
else:
  guilda.save()

logging.debug("Guilda: " + str(guilda) + " inserida no banco de dados")

aux = 0
for member in guild.members:
  

  if member['character'].level == 100:

    nome_personagem = str(member['character'].name)

    aux+=1 #TODO DELETAR ESSA PORRA

    print nome_personagem, ", ", member['character'].level
    membro_all = connection.get_character(nome_battlegroup, nome_realm, nome_personagem, fields=[Character.ITEMS, Character.TALENTS])

    criarEquipamento(membro_all.equipment.head)

    membro, created = Personagem.objects.get_or_create(nome = nome_personagem,
                          identificador = str(nome_personagem) + "@" + str(guild.name),
                          defaults={'ilvl_equipado' : int(membro_all.equipment.average_item_level_equipped),
                                    'guilda' : guilda,
                                    'head' : criarEquipamentos(membro_all.equipment.head),
                                    'shoulder' : membro_all.equipment.shoulder,
                                    'back' : membro_all.equipment.back,
                                    'chest': membro_all.equipment.chest,
                                    'wrist' : membro_all.equipment.wrist,
                                    'hands' : membro_all.equipment.hands ,
                                    'waist' : membro_all.equipment.waist,
                                    'legs' : membro_all.equipment.legs,
                                    'feet' : membro_all.equipment.feet,
                                    'finger1' : membro_all.equipment.finger1,
                                    'finger2' : membro_all.equipment.finger2,
                                    'trinket1' : membro_all.equipment.trinket1,
                                    'trinket2' : membro_all.equipment.trinket2,
                                    'main_hand' : membro_all.equipment.main_hand,
                                    'off_hand' : membro_all.equipment.off_hand})
    print 

    membro.save()


  if aux == 1:  #TODO DELETAR ESSA PORRA
    break       #TODO DELETAR ESSA PORRA




