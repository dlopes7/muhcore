# -*- coding: utf-8 -*-

import os, traceback

os.environ['PYTHONPATH'] = '/home/david/Documents/projeto/muhcore'
os.environ['DJANGO_SETTINGS_MODULE'] = 'muhcore.settings'

import django
from muh_core_app.models import Equipamento, Bis, Personagem, Guilda, Boss
from django.db.models import Q
from collections import defaultdict

django.setup()

test_bis = True
teste_boss = False

classes = {  # 'Death Knight':{'Blood', 'Unholy', 'Frost'}}
    # 'Druid':{'Blood', 'Unholy', 'Frost'},
    'Hunter': ['Beast Mastery'],
    # 'Mage':{'Blood', 'Unholy', 'Frost'},
    'Monk': ['Windwalker', 'Mistweaver'],
    'Paladin': ['Holy'],
    'Priest': ['Discipline'],
    # 'Rogue':{'Blood', 'Unholy', 'Frost'},
    'Shaman': ['Enhancement', 'Elemental']}


# 'Warlock':{'Blood', 'Unholy', 'Frost'},
# 'Warrior':{'Blood', 'Unholy', 'Frost'}



def get_boss(boss_id, guilda_id):
    # Get all equipment that drops from boss 'biss_id'
    items_from_boss = Equipamento.objects.filter(dropped_by=Boss.objects.get(pk=boss_id))
    lista_items_from_boss_id = list(item.wowhead_identificador for item in items_from_boss)

    guilda = Guilda.objects.get(pk=guilda_id)
    membros = guilda.personagem_guilda.all()

    membros_needed = defaultdict(list)

    for membro in membros:
        try:
            bis_needed = membro.get_bis_missing()
            for item in bis_needed:
                if item.wowhead_identificador in lista_items_from_boss_id:
                    membros_needed[membro].append(item)
        except Bis.DoesNotExist:
            # print ('No BIS found for ', membro.classe, membro.spec)
            continue

    return membros_needed


if test_bis:
    for classe, specs in classes.items():
        for spec in specs:
            jogadores = Personagem.objects.filter(Q(classe=classe) & Q(spec=spec),
                                                  guilda=Guilda.objects.get(nome='Defiant'))

            for jogador in jogadores:
                print('Bis que', jogador.nome, 'já tem:', '(' + classe + ' - ' + spec + ')')
                for bis in jogador.get_bis_equipped():
                    print(bis.dropped_by, ' - ', bis)

                print()
                print('Bis que', jogador.nome, 'não tem:', '(' + classe + ' - ' + spec + ')')
                for bis in jogador.get_bis_missing():
                    print(bis.dropped_by, ' - ', bis)
                print()

if teste_boss:
    bosses = Boss.objects.all()
    guilda = Guilda.objects.get(nome='Defiant')

    for boss in bosses:
        need_boss = get_boss(boss.id, guilda.id)
        print('Members who need', boss.nome)
        for nome, lista in need_boss.items():
            print(nome)
        print()
