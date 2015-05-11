# -*- coding: utf-8 -*-

import os, traceback

os.environ['PYTHONPATH'] = '/home/david/Documents/projeto/muhcore'
os.environ['DJANGO_SETTINGS_MODULE'] = 'muhcore.settings'


import codecs
import urllib.request
import sys
import battlenet
import operator
import logging
import django
import re


from collections import Counter

from battlenet import Connection, Character, Guild, EquippedItem
from muh_core_app.models import Personagem, Guilda, Equipamento, Historico
from django.utils import timezone



with_members = True

def criarEquipamento(equipamento_id): 
  if (equipamento_id != None):
    try:
      equip_exists = Equipamento.objects.get(identificador=equipamento_id)
      return equip_exists
    except Equipamento.DoesNotExist:
      print ('Criando Equipamento... ID:', equipamento_id)
      equipamento = EquippedItem(region, connection.get_item(region, equipamento_id))

      bonus_id = str(equipamento.bonus).replace("[", "").replace("]", "").replace(" ", "").replace(",", "")

      #print str(equipamento.id) + str(bonus_id)
      equip_criado, created = Equipamento.objects.get_or_create(identificador = int(str(equipamento.id) + str(bonus_id)),
                                                        defaults={'nome': equipamento.name,
                                                        'ilvl': int(equipamento.ilvl),
                                                        'bonus' :  equipamento.bonus,
                                                        'wowhead_identificador': equipamento.id,
                                                        'slot': equipamento.slot,
                                                        'origem': equipamento.context})

      equip_criado.save()
      return equip_criado
  else:
    return None

def criarBis(lista_bis):
  if (lista_bis != None ):
    print('oi')


django.setup()

logging.basicConfig(filename='../../processo.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

connection = battlenet.Connection(public_key='nm3jrgp8avwjpqnptby38z763t9afyes', private_key='Edt6pnruq8ntrE4YnwnBX4ckBnMddbf8', locale='en')

classes = {#'Death Knight':{'Blood', 'Unholy', 'Frost'}}
          #'Druid':{'Blood', 'Unholy', 'Frost'},
          #'Hunter':{'Blood', 'Unholy', 'Frost'},
          #'Mage':{'Blood', 'Unholy', 'Frost'},
          #'Monk':{'Blood', 'Unholy', 'Frost'},
          #'Paladin':{'Blood', 'Unholy', 'Frost'},
          #'Priest':{'Blood', 'Unholy', 'Frost'},
          #'Rogue':{'Blood', 'Unholy', 'Frost'},
          'Shaman':['Enhancement', 'Elemental']}
          #'Warlock':{'Blood', 'Unholy', 'Frost'},
          #'Warrior':{'Blood', 'Unholy', 'Frost'}

colors = {'Death Knight':'#C41F3B',
          'Druid':'#FF7D0A',
          'Hunter':'#ABD473',
          'Mage':'#69CCF0',
          'Monk':'#00FF96',
          'Paladin':'#F58CBA',
          'Priest':'#FFFFFF',
          'Rogue':'#FFF569',
          'Shaman':'#0070DE',
          'Warlock':'#9482C9',
          'Warrior':'#C79C6E'}

bis_list = {'Shaman - Elemental'  : [113904, 113960, 115579, 113872, 115576, 120078, 115577, 113968, 115578, 113955, 113944, 113954, 113975, 118306, 113948, 113984],
            'Shaman - Enhancement': [113897, 113897, 113892, 113929, 119334, 113930, 113944, 113888, 118307, 113877, 113931, 118114, 115579, 115576, 115577, 115578]}






region = battlenet.UNITED_STATES
 ## http://imgur.com/InLkJUj


for classe, specs in classes.items():
  for spec in specs:
    print (classe, spec)
    bis_spec = bis_list[classe + ' - ' + spec]
    for bis in bis_spec:
      equip_exists = criarEquipamento(bis)
      print (equip_exists)
