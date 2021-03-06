# -*- coding: utf-8 -*-

import os
import traceback

os.environ['PYTHONPATH'] = '/home/david/Documents/projeto/muhcore'
os.environ['DJANGO_SETTINGS_MODULE'] = 'muhcore.settings'


import urllib.request
import battlenet
import logging
import django
import re

from collections import Counter

from battlenet import Connection, Character, Guild
from muh_core_app.models import Personagem, Guilda, Equipamento, Historico, Boss
from django.utils import timezone
from wowheadhelper import get_item_source

#-------------------Guilda a ser scaneada -------
#nome_guilda = 'Taunta Que Eu Aggrei'
#nome_realm = 'Azralon'
#nome_battlegroup = battlenet.UNITED_STATES
#------------------------------------------------
region = battlenet.UNITED_STATES

array_guildas = [#['Midwinter', 'Sargeras', battlenet.UNITED_STATES],
        #['Avast', 'Jubei\'Thos', battlenet.UNITED_STATES],
        #['Ascension','Barthilas', battlenet.UNITED_STATES],
        #['Duality', 'Zul\'jin', battlenet.UNITED_STATES],
        #['Huge in Japan', 'Kil\'Jaeden', battlenet.UNITED_STATES],
        #['Reckoning', 'Mannoroth', battlenet.UNITED_STATES],
        #['Honestly', 'Frostmourne', battlenet.UNITED_STATES],
        #['Limit', 'Illidan', battlenet.UNITED_STATES],
        #['Razzia', 'Arthas', battlenet.UNITED_STATES],
        #['Smitus and Friends', 'Sargeras', battlenet.UNITED_STATES],
        #['vodka', 'Stormrage', battlenet.UNITED_STATES],
        #['WHATEVER WERE AWESOME', 'Magtheridon', battlenet.UNITED_STATES],
        #['Encore', 'Illidan', battlenet.UNITED_STATES],
        #['Promethean', 'Stormreaver', battlenet.UNITED_STATES],
        #['Raiding Rainbows', 'Illidan', battlenet.UNITED_STATES],
        #['Vigil', 'Mal\'Ganis', battlenet.UNITED_STATES],
        #['Shake Miracle', 'Illidan', battlenet.UNITED_STATES],
        #['KLG Rising', 'Ragnaros', battlenet.UNITED_STATES],
        #['Strawberry Puppy Kisses', 'Area 52', battlenet.UNITED_STATES],
        ['Defiant', 'Azralon', battlenet.UNITED_STATES]]

with_members = True
ignore_wowrprogress = False

def get_boss(boss_nome):
  
  if boss_nome == None:
    boss_nome = 'None'
  
  try:
    boss_exists = Boss.objects.get(nome = boss_nome)
  except Boss.DoesNotExist:
    boss_exists = Boss.objects.create(nome = boss_nome)
  return boss_exists

def criarEquipamento(equipamento):
  if (equipamento != None):

    
    bonus_id = str(equipamento.bonus).replace("[", "").replace("]", "").replace(" ", "").replace(",", "")
    identificador_equipamento = int(str(equipamento.id) + str(bonus_id))
    slot = equipamento.slot
    dropped_by_boss = None

    print (equipamento.name)


    #Always faster to get info locally than from battle.net
    try:
      equip_criado = Equipamento.objects.get(identificador=identificador_equipamento)
      return equip_criado

    except Equipamento.DoesNotExist:
      if slot == None:
        try:
          slot = Equipamento.objects.get(identificador=equipamento.id).slot
          dropped_by_boss = Equipamento.objects.get(identificador=equipamento.id).dropped_by
          print (dropped_by_boss)
        except Equipamento.DoesNotExist:
          print ('No slot found, getting item from battle.net')
          equipamento.slot = connection.get_item(region, equipamento.id)['inventoryType']

      equip_criado = Equipamento.objects.create(identificador = identificador_equipamento)

      equip_criado.nome = equipamento.name
      equip_criado.ilvl = int(equipamento.ilvl)
      equip_criado.bonus =  equipamento.bonus
      equip_criado.wowhead_identificador = equipamento.id
      equip_criado.slot = slot
      equip_criado.origem = equipamento.context
      equip_criado.dropped_by = dropped_by_boss
      equip_criado.save()

      return equip_criado


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



for processar_guilda in array_guildas:
  nome_guilda = processar_guilda[0]
  nome_realm = processar_guilda[1]
  nome_battlegroup = processar_guilda[2]

  print("Guilda: " + nome_guilda + ", Realm: " + nome_realm + " BG: " + str(nome_battlegroup))
  if not ignore_wowrprogress:
    print ("Conectando ao WoWProgress")
    url_wowprogress = "http://www.wowprogress.com/guild/"+ nome_battlegroup +"/"+ nome_realm.replace(' ', '-').replace('\'', '-') + "/" + nome_guilda
    print (url_wowprogress)
    pagina = urllib.request.urlopen(url_wowprogress)
    print ("Conectado!")

    conteudo = pagina.read().decode("utf-8")
    id_wowprogress = str(re.search('/guild_img/(.*?)"',conteudo).group(1))#.replace('\'', '')[1:]
    url_wowprogress_icon = "http://www.wowprogress.com/guild_img/" + id_wowprogress + "/out/type.site"

    # class="innerLink ratingProgress" id="gk346_1034420"><b>6/7 (M)</b>  9/10 (H)</span>
    progresso = str(re.search('ratingProgress.*?<b>(.*?)</span>',conteudo).group(1))
    progresso = progresso.replace("</b>", "").replace("<b>", "- ")#.replace('\'', '')[1:]
    print ("Progresso", progresso)


    urllib.request.urlretrieve(url_wowprogress_icon, 'muh_core_app/static/img/wowprogress/' + id_wowprogress+'.jpg')

  logging.debug("Conectando a battlenet")
  print ("Conectando a battlenet...")
  guild = connection.get_guild(nome_battlegroup, nome_realm, nome_guilda, fields=[Guild.MEMBERS])
  print ("Conectado!")
  #print(guild)
  id_guilda = str(guild.name) + "@" + str(guild.realm)

  try:
    guilda = Guilda.objects.get(identificador = id_guilda)
  except Guilda.DoesNotExist:
    guilda = Guilda.objects.create(identificador = id_guilda,
                                                nome = str(guild.name),
                                                reino = str(guild.realm))

  if not ignore_wowrprogress:
    guilda.num_membros = len(guild.members)
    guilda.wowprogress_id = id_wowprogress
    guilda.progresso = progresso

  guilda.save()
  
  print ("Guilda: " + str(guilda) + " inserida no banco de dados")

  print (len(guild.members), "membros")

  if not with_members:
    continue

  
  for member in guild.members:
    if member['character'].level == 100 and member['rank'] <= 3:
      nome_personagem = str(member['character'].name)

      print()
      print (nome_personagem)

      try: 
        membro_all = connection.get_character(nome_battlegroup, nome_realm, nome_personagem, fields=[Character.ITEMS, Character.TALENTS])
        print (membro_all.get_class_name(), membro_all.get_spec_name(), membro_all.equipment.average_item_level_equipped)
          #hue 

        membro, created = Personagem.objects.get_or_create(nome = nome_personagem,
                              identificador = str(nome_personagem) + "@" + str(guild.name),
                              defaults={'ilvl_equipado' : int(membro_all.equipment.average_item_level_equipped),
                                        'color' : colors[membro_all.get_class_name()],
                                        'classe' : membro_all.get_class_name(),
                                        'spec' : membro_all.get_spec_name(),
                                        'icon_spec' : membro_all.get_spec_icon(),
                                        'avatar' : membro_all.get_thumbnail_url(),
                                        'guilda' : guilda,
                                        'head' : criarEquipamento(membro_all.equipment.head),
                                        'shoulder' : criarEquipamento(membro_all.equipment.shoulder),
                                        'neck' : criarEquipamento(membro_all.equipment.neck),
                                        'back' : criarEquipamento(membro_all.equipment.back),
                                        'chest': criarEquipamento(membro_all.equipment.chest),
                                        'wrist' : criarEquipamento(membro_all.equipment.wrist),
                                        'hands' : criarEquipamento(membro_all.equipment.hands),
                                        'waist' : criarEquipamento(membro_all.equipment.waist),
                                        'legs' : criarEquipamento(membro_all.equipment.legs),
                                        'feet' : criarEquipamento(membro_all.equipment.feet),
                                        'finger1' : criarEquipamento(membro_all.equipment.finger1),
                                        'finger2' :  criarEquipamento(membro_all.equipment.finger2),
                                        'trinket1' : criarEquipamento(membro_all.equipment.trinket1),
                                        'trinket2' : criarEquipamento(membro_all.equipment.trinket2),
                                        'main_hand' : criarEquipamento(membro_all.equipment.main_hand),
                                        'off_hand' : criarEquipamento(membro_all.equipment.off_hand)})
      
        if not created:
          #print 'OPA ja existe', membro.ilvl_equipado, 

          membro.ilvl_equipado = int(membro_all.equipment.average_item_level_equipped)
          membro.spec = membro_all.get_spec_name()
          membro.icon_spec = membro_all.get_spec_icon()
          membro.avatar = membro_all.get_thumbnail_url()
          membro.guilda = guilda
          membro.head = criarEquipamento(membro_all.equipment.head)
          membro.shoulder = criarEquipamento(membro_all.equipment.shoulder)
          membro.neck = criarEquipamento(membro_all.equipment.neck)
          membro.back = criarEquipamento(membro_all.equipment.back)
          membro.chest = criarEquipamento(membro_all.equipment.chest)
          membro.wrist = criarEquipamento(membro_all.equipment.wrist)
          membro.hands = criarEquipamento(membro_all.equipment.hands)
          membro.waist = criarEquipamento(membro_all.equipment.waist)
          membro.legs = criarEquipamento(membro_all.equipment.legs)
          membro.feet = criarEquipamento(membro_all.equipment.feet)
          membro.finger1 = criarEquipamento(membro_all.equipment.finger1)
          membro.finger2 =criarEquipamento(membro_all.equipment.finger2)
          membro.trinket1 = criarEquipamento(membro_all.equipment.trinket1)
          membro.trinket2 = criarEquipamento(membro_all.equipment.trinket2)
          membro.main_hand = criarEquipamento(membro_all.equipment.main_hand)
          membro.off_hand = criarEquipamento(membro_all.equipment.off_hand)
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




