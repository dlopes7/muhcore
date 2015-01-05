from django.db import models
from django.db.models import Avg, Max, Min

from math import floor

# Create your models here.

class Guilda(models.Model):
    nome = models.CharField(max_length=200)
    reino = models.CharField(max_length=200)
    identificador = models.CharField(max_length=200)
    num_membros = models.IntegerField()

    def get_membros_lvl_100(self):
        return len(self.personagem_guilda.all())

    def get_ilvl_medio(self):
        return int(floor(self.personagem_guilda.all().aggregate(Avg('ilvl_equipado'))['ilvl_equipado__avg']))

    def get_maior_ilvl(self):
        return int(floor(self.personagem_guilda.all().aggregate(Max('ilvl_equipado'))['ilvl_equipado__max']))

    def get_menor_ilvl(self):
        return int(floor(self.personagem_guilda.all().aggregate(Min('ilvl_equipado'))['ilvl_equipado__min']))


    def __str__(self):
    	return self.nome + "@" + self.reino

class Equipamento(models.Model):
    nome = models.CharField(max_length=200)
    slot = models.CharField(max_length=200)
    ilvl = models.IntegerField()
    bonus = models.CharField(max_length=200)
    origem = models.CharField(max_length=200)
    identificador = models.CharField(max_length=300)
    wowhead_identificador = models.CharField(max_length=200)
    def __str__(self):
	   return self.nome

    def get_bonus(self):
        bonus = self.bonus.replace("[", "").replace("]", "").replace(" ", "").replace(",", ":")
        return str(bonus)


class Personagem(models.Model):
    nome = models.CharField(max_length=200)
    ilvl_equipado = models.IntegerField()
    identificador = models.CharField(max_length=200)
    avatar = models.CharField(max_length=800)
    color = models.CharField(max_length=200, default='1')

    classe = models.CharField(max_length=200, default='1')
    spec = models.CharField(max_length=200, default='1')
    icon_spec = models.CharField(max_length=600, default='1')


    guilda =  models.ForeignKey(Guilda, related_name='personagem_guilda', null=True, blank=True)
    head = models.ForeignKey(Equipamento, related_name='personagem_head', null=True, blank=True)
    shoulder = models.ForeignKey(Equipamento, related_name='personagem_shoulder', null=True, blank=True)
    neck = models.ForeignKey(Equipamento, related_name='personagem_neck', null=True, blank=True)
    back = models.ForeignKey(Equipamento, related_name='personagem_back', null=True, blank=True)
    chest = models.ForeignKey(Equipamento, related_name='personagem_chest', null=True, blank=True)
    wrist = models.ForeignKey(Equipamento, related_name='personagem_wrist', null=True, blank=True)
    hands = models.ForeignKey(Equipamento, related_name='personagem_hands', null=True, blank=True)
    waist = models.ForeignKey(Equipamento, related_name='personagem_waist', null=True, blank=True)
    legs = models.ForeignKey(Equipamento, related_name='personagem_legs', null=True, blank=True)
    feet = models.ForeignKey(Equipamento, related_name='personagem_feet', null=True, blank=True)
    finger1 = models.ForeignKey(Equipamento, related_name='personagem_finger1', null=True, blank=True)
    finger2 = models.ForeignKey(Equipamento, related_name='personagem_finger2', null=True, blank=True)
    trinket1 = models.ForeignKey(Equipamento, related_name='personagem_trinket1', null=True, blank=True)
    trinket2 = models.ForeignKey(Equipamento, related_name='personagem_trinket2', null=True, blank=True)
    main_hand = models.ForeignKey(Equipamento, related_name='personagem_main_hand', null=True, blank=True)
    off_hand = models.ForeignKey(Equipamento, related_name='personagem_off_hand', null=True, blank=True)


    def __str__(self):
    	return self.nome


