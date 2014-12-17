# -*- coding: utf-8 -*-
import codecs
import urllib
import sys
import battlenet
import operator
from collections import Counter

from battlenet import Connection
from battlenet import Character
from battlenet import Guild

#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')

connection = Connection(public_key='nm3jrgp8avwjpqnptby38z763t9afyes', private_key='Edt6pnruq8ntrE4YnwnBX4ckBnMddbf8', locale='en')


nome_guilda = 'Paragon'
nome_realm = 'Lightnings Blade'
nome_battlegroup = battlenet.EUROPE

print 'Conectando nessa porra'
guild = connection.get_guild(nome_battlegroup, nome_realm, nome_guilda, fields=[Guild.MEMBERS])
#guild = connection.get_guild(battlenet.UNITED_STATES, 'Azralon', 'Taunta Que Eu Aggrei', fields=[Guild.MEMBERS])

print "Guild ", guild.name

caras = {}

#print "Membros nivel 100:", guild.members.count("level\":100")

nvl100 = 0

##1 warrior
##2 paladin
##3 hunter
##4 rogue
##5 priest
##6 DK
##7 Shaman
##8 mage
##9 warlock
##10 monk
##11 druid


classes = {1:'Warrior',
           2:'Paladin',
           3:'Hunter',
           4:'Rogue',
           5:'Priest',
           6:'Death Knight',
           7:'Shaman',
           8:'Mage',
           9:'Warlock',
           10:'Monk',
           11:'Druid'}

comp = {'Warrior':0,
           'Paladin':0,
           'Hunter':0,
           'Rogue':0,
           'Priest':0,
           'Death Knight':0,
           'Shaman':0,
           'Mage':0,
           'Warlock':0,
           'Monk':0,
           'Druid':0}

for member in guild.members:
    level = member['character'].level

    
    if(level == 100):
        classe = member['character'].class_
        comp[classes[classe]] += 1
        nvl100+=1

print "Numero de membros nivel 100:", str(nvl100) + "/" + str(len(guild.members))
for classe, qtd in comp.iteritems() :
    print qtd, classe
    

aux = 0

for member in guild.members:
    #print member['character'].name
    #print member['character'].name.decode('utf-8')
   # print urllib.quote(member['character'].name)
    #print urllib.quote(member['character'].name).decode('utf-8')
    
    #name =  urllib.quote(member['character'].name).decode('utf-8')
    name =  member['character'].name.decode('utf-8')
    
    #print name
    level = member['character'].level

    classe = ''
    spec = ''

    if(level == 100):
        try:
            aux +=1
            print "\nProcessando o macaco", name, str(aux) + "/" + str(nvl100)
            character = connection.get_character(nome_battlegroup, nome_realm, name, fields=[Character.ITEMS, Character.TALENTS])
        except Exception, e:
            continue
        try:
            if (character.level == 100):
                
                classe = character.get_class_name()
                spec =  character.get_spec_name()
                print classe, spec
                #print character.get_class_name(), character.get_spec_name()

                #print "TO INSERINDO ESSA PORRA", name
                caras[name + ": " + classe+" "+ spec] = int(character.equipment.average_item_level_equipped)
                #print "INSERI ESSA PORRA", caras
                print "ilvl:\t", character.equipment.average_item_level, "\nEilvl:\t", character.equipment.average_item_level_equipped

        except Exception, e:
            print e
            continue

sorted_caras = sorted(caras.items(), key=operator.itemgetter(1), reverse=True)

_600menos = 0
_600_610= 0
_610_620= 0
_620_630= 0
_630mais= 0

for m in sorted_caras:
    print m[0], m[1]
    if int(m[1]) < 600:
        _600menos+=1
    if int(m[1]) > 600 and int(m[1]) < 610:
        _600_610+=1
    if int(m[1]) > 610 and int(m[1]) < 620:
        _610_620+=1
    if int(m[1]) > 620 and int(m[1]) < 630:
        _620_630+=1
    if int(m[1]) > 630:
        _630mais+=1

print "Menos de 600 ilvl", _600menos
print "De 600 a 610", _600_610
print "De 610 a 620", _610_620
print "De 620 a 630", _620_630
print "Mais de 630", _630mais






