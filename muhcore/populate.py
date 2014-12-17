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

logging.basicConfig(filename='processo.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')


connection = battlenet.Connection(public_key='nm3jrgp8avwjpqnptby38z763t9afyes', private_key='Edt6pnruq8ntrE4YnwnBX4ckBnMddbf8', locale='en')

nome_guilda = 'Paragon'
nome_realm = 'Lightnings Blade'
nome_battlegroup = battlenet.EUROPE

logging.debug("Guilda: " + nome_guilda + ", Realm: " + nome_realm + " BG: " + str(nome_battlegroup))

logging.debug("Conectando a battlenet")
guild = connection.get_guild(nome_battlegroup, nome_realm, nome_guilda, fields=[Guild.MEMBERS])
logging.debug("Conectado!")


guilda = Guilda(nome = str(guild.name), reino = str(guild.realm), identificador = str(guild.name) + "@" + str(guild.realm)) 
guilda.save()

logging.debug("Guilda: " + str(guilda) + " inserida no banco de dados")

print Guilda.objects.all()


