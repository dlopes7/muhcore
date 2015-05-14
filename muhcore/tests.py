# -*- coding: utf-8 -*-

import os, traceback

os.environ['PYTHONPATH'] = '/home/david/Documents/projeto/muhcore'
os.environ['DJANGO_SETTINGS_MODULE'] = 'muhcore.settings'

import django
from muh_core_app.models import Equipamento, Bis, Personagem, Guilda, Boss

django.setup()

test_bis = False
test_boss = True




classes = {#'Death Knight':{'Blood', 'Unholy', 'Frost'}}
          #'Druid':{'Blood', 'Unholy', 'Frost'},
          #'Hunter':{'Blood', 'Unholy', 'Frost'},
          #'Mage':{'Blood', 'Unholy', 'Frost'},
          'Monk':['Windwalker', 'Mistweaver'],
          'Paladin':['Holy'],
          'Priest':['Discipline'],
          #'Rogue':{'Blood', 'Unholy', 'Frost'},
          'Shaman':['Enhancement', 'Elemental']}
          #'Warlock':{'Blood', 'Unholy', 'Frost'},
          #'Warrior':{'Blood', 'Unholy', 'Frost'}




if test_bis:
  for classe, specs in classes.items():
    for spec in specs:
      jogadores = Personagem.objects.filter(classe = classe, spec = spec, guilda = Guilda.objects.get(nome = 'Defiant'))

      for jogador in jogadores:
        print ('Bis que', jogador.nome, 'já tem:', '(' + classe + ' - ' + spec + ')')
        for bis in jogador.get_bis_equipped():
          if bis != None:
            print (Equipamento.objects.get(identificador = bis))

        print()
        print ('Bis que', jogador.nome, 'não tem:', '(' + classe + ' - ' + spec + ')')
        for bis in jogador.get_bis_missing():
          if bis != None:
            print (Equipamento.objects.get(identificador = bis))
        print()



if test_boss:
  player = Personagem.objects.get(nome = 'Gordonfreema')
  for bis in player.get_bis_missing():
    if bis != None:
      item = Equipamento.objects.get(identificador = bis)
      boss = item.dropped_by.nome
      print (boss, item)
