# -*- coding: utf-8 -*-


import urllib.request
import re
import json


def get_item_source(item_id):
    dropped_by = None

    url_wowhead = 'http://www.wowhead.com/item=' + str(item_id)
    pagina = urllib.request.urlopen(url_wowhead)
    conteudo = pagina.read().decode("utf-8")

    match_boss = re.search('Dropped by:(.*?)<', conteudo)
    if match_boss != None:
        dropped_by = str(match_boss.group(1)).strip()

    return dropped_by


def get_boss_drops(boss_id):
    # http://www.wowhead.com/npc=76877#drops:mode=m


    url_wowhead = 'http://www.wowhead.com/npc=' + str(boss_id) + '#drops:mode=m'
    pagina = urllib.request.urlopen(url_wowhead)
    conteudo = pagina.read().decode("utf-8")

    # print (conteudo)


    match_boss = re.search('onAfterCreate: Listview.funcBox.addModeIndicator, data: \[(.*?)\}\]\}', conteudo)
    if match_boss != None:
        data_items = (str(match_boss.group(1)) + '}').split('reqlevel')

        lista_items = []

        for i in data_items:
            # "id":113864,
            item_id = re.search('"id"\:(.*?),', i)
            item_lvl = re.search('"level"\:(.*?),', i)
            item_name = re.search('"name"\:"(.*?)",', i)
            if item_id != None and item_lvl != None and item_name != None:
                lista_items.append(item_id.group(1))
        return lista_items

        # "name":"(.*?)"
        # "level":(.*?),

        # return dropped_by


get_boss_drops(76877)
