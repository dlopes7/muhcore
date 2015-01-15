# -*- coding: utf-8 -*-

import os, traceback

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
from muh_core_app.models import Personagem, Guilda, Equipamento, Historico
from django.utils import timezone

#-------------------Guilda a ser scaneada -------
nome_guilda = 'Taunta Que Eu Aggrei'
nome_realm = 'Azralon'
nome_battlegroup = battlenet.UNITED_STATES
#------------------------------------------------


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



logging.debug("Guilda: " + nome_guilda + ", Realm: " + nome_realm + " BG: " + str(nome_battlegroup))

logging.debug("Conectando a battlenet")
print "Conectando a battlenet..."
guild = connection.get_guild(nome_battlegroup, nome_realm, nome_guilda, fields=[Guild.MEMBERS])
print "Conectado!"


guilda, created = Guilda.objects.get_or_create(nome = str(guild.name),
                                               reino = str(guild.realm),
                                               identificador = str(guild.name) + "@" + str(guild.realm),
                                               defaults = {'num_membros': len(guild.members)}) 

if not created:
  guilda.save() 
else:
  guilda.save()

print "Guilda: " + str(guilda) + " inserida no banco de dados"

print len(guild.members), "membros"

aux = 0
for member in guild.members:
  if member['character'].level == 100:
    nome_personagem = str(member['character'].name)
    aux+=1 #TODO DELETAR ESSA PORRA

    print nome_personagem,

    try: 
      membro_all = connection.get_character(nome_battlegroup, nome_realm, nome_personagem, fields=[Character.ITEMS, Character.TALENTS])
      print membro_all.get_class_name(), membro_all.get_spec_name(), membro_all.equipment.average_item_level_equipped


      membro, created = Personagem.objects.get_or_create(nome = nome_personagem,
                            identificador = str(nome_personagem) + "@" + str(guild.name),
                            defaults={'ilvl_equipado' : int(membro_all.equipment.average_item_level_equipped),
                                      'color' : colors[membro_all.get_class_name()],
                                      'classe' : membro_all.get_class_name(),
                                      'spec' : membro_all.get_spec_name(),
                                      'icon_spec' : membro_all.get_spec_icon(),
                                      'avatar' : membro_all.get_thumbnail_url(),
                                      'guilda' : guilda,
                                      'head' : criarEquipamento(membro_all.equipment.head, 'head'),
                                      'shoulder' : criarEquipamento(membro_all.equipment.shoulder, 'shoulder'),
                                      'neck' : criarEquipamento(membro_all.equipment.shoulder, 'neck'),
                                      'back' : criarEquipamento(membro_all.equipment.back, 'back'),
                                      'chest': criarEquipamento(membro_all.equipment.chest, 'chest'),
                                      'wrist' : criarEquipamento(membro_all.equipment.wrist, 'wrist'),
                                      'hands' : criarEquipamento(membro_all.equipment.hands , 'hands'),
                                      'waist' : criarEquipamento(membro_all.equipment.waist, 'waist'),
                                      'legs' : criarEquipamento(membro_all.equipment.legs, 'legs'),
                                      'feet' : criarEquipamento(membro_all.equipment.feet, 'feet'),
                                      'finger1' : criarEquipamento(membro_all.equipment.finger1, 'finger1'),
                                      'finger2' :  criarEquipamento(membro_all.equipment.finger2, 'finger2'),
                                      'trinket1' : criarEquipamento(membro_all.equipment.trinket1, 'trinket1'),
                                      'trinket2' : criarEquipamento(membro_all.equipment.trinket2, 'trinket2'),
                                      'main_hand' : criarEquipamento(membro_all.equipment.main_hand, 'main_hand'),
                                      'off_hand' : criarEquipamento(membro_all.equipment.off_hand, 'off_hand')})
    
      if not created:
        #print 'OPA ja existe', membro.ilvl_equipado, 

        membro.ilvl_equipado = int(membro_all.equipment.average_item_level_equipped)
        membro.spec = membro_all.get_spec_name()
        membro.icon_spec = membro_all.get_spec_icon()
        membro.avatar = membro_all.get_thumbnail_url()
        membro.guilda = guilda
        membro.head = criarEquipamento(membro_all.equipment.head, 'head')
        membro.shoulder = criarEquipamento(membro_all.equipment.shoulder, 'shoulder')
        membro.neck = criarEquipamento(membro_all.equipment.shoulder, 'neck')
        membro.back = criarEquipamento(membro_all.equipment.back, 'back')
        membro.chest = criarEquipamento(membro_all.equipment.chest, 'chest')
        membro.wrist = criarEquipamento(membro_all.equipment.wrist, 'wrist')
        membro.hands = criarEquipamento(membro_all.equipment.hands , 'hands')
        membro.waist = criarEquipamento(membro_all.equipment.waist, 'waist')
        membro.legs = criarEquipamento(membro_all.equipment.legs, 'legs')
        membro.feet = criarEquipamento(membro_all.equipment.feet, 'feet')
        membro.finger1 = criarEquipamento(membro_all.equipment.finger1, 'finger1')
        membro.finger2 =criarEquipamento(membro_all.equipment.finger2, 'finger2')
        membro.trinket1 = criarEquipamento(membro_all.equipment.trinket1, 'trinket1')
        membro.trinket2 = criarEquipamento(membro_all.equipment.trinket2, 'trinket2')
        membro.main_hand = criarEquipamento(membro_all.equipment.main_hand, 'main_hand')
        membro.off_hand = criarEquipamento(membro_all.equipment.off_hand, 'off_hand')
        #print membro.ilvl_equipado

      #print membro, created

      
      membro.save()

      historico = Historico.objects.get_or_create(data = timezone.now(), defaults = {'personagem': membro,
                                                              'ilvl_equipado': membro.ilvl_equipado})
    except:
      traceback.print_exc()
      continue


  #if aux == 20:  #TODO DELETAR ESSA PORRA
  #  break       #TODO DELETAR ESSA PORRA




