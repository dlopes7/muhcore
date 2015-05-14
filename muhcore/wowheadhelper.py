# -*- coding: utf-8 -*-


import urllib.request
import re

def get_item_source(item_id):

  dropped_by = None

  url_wowhead = 'http://www.wowhead.com/item=' + str(item_id)
  pagina = urllib.request.urlopen(url_wowhead)
  conteudo = pagina.read().decode("utf-8")


  match_boss = re.search('Dropped by:(.*?)<',conteudo)
  if match_boss != None:
    dropped_by = str(match_boss.group(1)).strip()

  return dropped_by


