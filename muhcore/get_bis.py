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

from battlenet import Connection, Character, Guild
from muh_core_app.models import Personagem, Guilda, Equipamento, Historico
from django.utils import timezone
from bs4 import BeautifulSoup


with_members = True

def criarEquipamento(equipamento, slot):
  if (equipamento != None):
    bonus_id = str(equipamento.bonus).replace("[", "").replace("]", "").replace(" ", "").replace(",", "")

    #print str(equipamento.id) + str(bonus_id)
    equip_criado, created = Equipamento.objects.get_or_create(identificador = int(str(equipamento.id) + str(bonus_id)),
                                                        defaults={'nome': equipamento.name,
                                                        'ilvl': int(equipamento.ilvl),
                                                        'bonus' :  equipamento.bonus,
                                                        'wowhead_identificador': equipamento.id,
                                                        'slot': slot,
                                                        'origem': equipamento.context})

    equip_criado.save()
      #print equip_criado.origem  
    #print equip_criado.wowhead_identificador, equipamento.id
      #print equip_criado.get_bonus()
    return equip_criado
  else:
    return None


django.setup()

logging.basicConfig(filename='../../processo.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

connection = battlenet.Connection(public_key='nm3jrgp8avwjpqnptby38z763t9afyes', private_key='Edt6pnruq8ntrE4YnwnBX4ckBnMddbf8', locale='en')

classes = {'Death Knight':{'Blood', 'Unholy', 'Frost'}}
          #'Druid':{'Blood', 'Unholy', 'Frost'},
          #'Hunter':{'Blood', 'Unholy', 'Frost'},
          #'Mage':{'Blood', 'Unholy', 'Frost'},
          #'Monk':{'Blood', 'Unholy', 'Frost'},
          #'Paladin':{'Blood', 'Unholy', 'Frost'},
          #'Priest':{'Blood', 'Unholy', 'Frost'},
          #'Rogue':{'Blood', 'Unholy', 'Frost'},
          #'Shaman':{'Blood', 'Unholy', 'Frost'},
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


 ## http://imgur.com/InLkJUj

def make_url(classe, spec):
  #http://www.wowbis.net/deathknight/blood/
  return 'http://www.wowbis.net/' + classe.replace(' ', '').lower() + '/' + spec.replace(' ', '').lower() + '/'

for classe, specs in classes.items():
  for spec in specs:
    print (classe, spec)
    url_wow_bis = make_url(classe, spec)

    print ("Conectando ao WoWBis: " + url_wow_bis)
    pagina = urllib.request.urlopen(url_wow_bis)

    conteudo = pagina.read().decode("utf-8")
    soup = BeautifulSoup(conteudo);

    div_items = soup.findAll('div', id=re.compile('^iteminfo_container'))
    for div_item in div_items:
      print (div_item[])

   

