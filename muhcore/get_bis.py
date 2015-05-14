# -*- coding: utf-8 -*-

import os, traceback

os.environ['PYTHONPATH'] = '/home/david/Documents/projeto/muhcore'
os.environ['DJANGO_SETTINGS_MODULE'] = 'muhcore.settings'


import battlenet
import django

from battlenet import Connection, EquippedItem
from muh_core_app.models import Equipamento, Bis, Boss
from wowheadhelper import get_item_source

def get_boss(boss_nome):
  
  if boss_nome == None:
    boss_nome = 'None'
  
  try:
    boss_exists = Boss.objects.get(nome = boss_nome)
  except Boss.DoesNotExist:
    boss_exists = Boss.objects.create(nome = boss_nome)
  return boss_exists

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
      equip_criado = Equipamento.objects.create(identificador = equipamento_id)

      equip_criado.nome = equipamento.name
      equip_criado.ilvl = int(equipamento.ilvl)
      equip_criado.bonus =  equipamento.bonus
      equip_criado.wowhead_identificador = equipamento.id
      equip_criado.slot = equipamento.slot
      equip_criado.origem = equipamento.context

      equip_criado.dropped_by = get_boss(get_item_source(equipamento_id))

      print('dropped by ', equip_criado.dropped_by.nome)
      print()

      equip_criado.save()

      return equip_criado
  else:
    return None

def criarBis(classe, spec, lista_bis):
  print ('Criando BIS para ', classe, spec)
  if (lista_bis != None ):
    try:
      bis_atual = Bis.objects.get(identificador=(classe) + " - " + (spec))
      print ('BIS para ', classe, spec, 'já existe, alterando items')
    except Bis.DoesNotExist:
      print ('BIS para ', classe, spec, 'ainda não existe, criando items')
      bis_atual = Bis.objects.create(identificador = (classe) + " - " + (spec),
                                      classe = classe,
                                      spec = spec)
      bis_atual.save()

    for bis_id in lista_bis:
      equipamento = Equipamento.objects.get(identificador=bis_id)
      bis_atual.add_equipment(equipamento)
      print (str(equipamento.identificador) + ' - ' + str(equipamento.nome))
    bis_atual.save()

django.setup()
connection = battlenet.Connection(public_key='nm3jrgp8avwjpqnptby38z763t9afyes', private_key='Edt6pnruq8ntrE4YnwnBX4ckBnMddbf8', locale='en')

classes = {#'Death Knight':{'Blood', 'Unholy', 'Frost'}}
          #'Druid':{'Blood', 'Unholy', 'Frost'},
          #'Hunter':{'Blood', 'Unholy', 'Frost'},
          #'Mage':{'Blood', 'Unholy', 'Frost'},
          #'Monk':['Windwalker', 'Mistweaver'],
          #'Paladin':['Holy'],
          #'Priest':['Discipline'],
          #'Rogue':{'Blood', 'Unholy', 'Frost'},
          'Shaman':['Enhancement', 'Elemental']}
          #'Warlock':{'Blood', 'Unholy', 'Frost'},
          #'Warrior':{'Blood', 'Unholy', 'Frost'}

bis_list = {'Shaman - Elemental'  : [113904, 113960, 115579, 113872, 115576, 120078, 115577, 113968,
                                     115578, 113955, 113944, 113954, 113975, 118306, 113948, 113984],

            'Shaman - Enhancement': [113897, 113897, 113892, 113929, 119334, 113930, 113944, 113888,
                                     118307, 113877, 113931, 118114, 115579, 115576, 115577, 115578],

            'Paladin - Holy':       [113934, 113946, 115568, 113890, 115565, 113878, 115566, 113896,
                                     113906, 113976, 115569, 119341, 113957, 118309, 113986, 119194],

            'Priest - Discipline':  [113904, 113960, 113981, 113890, 115561, 113945, 115560, 113887,
                                     115562, 113941, 115564, 113942, 113901, 118309, 113889, 113986],

            'Monk - Windwalker':    [113865, 113870, 113877, 113895, 113931, 113939, 113964, 113971,
                                     113985, 115555, 115556, 115557, 115559, 119333, 118307],

            'Monk - Mistweaver':    [113870,113878,113889,113895,113932,113957,113960,113964,113973,
                                     115555,115556,115557,115559,118309,119192,119333]}


with_members = True
region = battlenet.UNITED_STATES


for classe, specs in classes.items():
  for spec in specs:
    print (classe, spec)
    bis_spec_list = bis_list[classe + ' - ' + spec]

    for equipamento_id in bis_spec_list:
      equip_exists = criarEquipamento(equipamento_id)

    criarBis(classe, spec, bis_spec_list)
    print()

#TODO alguns equipamentos estao com slot = None