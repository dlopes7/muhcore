from django.db import models
from django.db.models import Avg, Max, Min

from math import floor
import datetime
from django.utils import timezone

# Create your models here.

class Boss(models.Model): 
    nome = models.CharField(max_length=200)

class Guilda(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    reino = models.CharField(max_length=200, null=True, blank=True)
    identificador = models.CharField(max_length=200)
    num_membros = models.IntegerField(null=True, blank=True)
    wowprogress_id = models.CharField(max_length=200, null=True, blank=True)
    progresso = models.CharField(max_length=50, null=True, blank=True)

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

    nome = models.CharField(max_length=200, null=True, blank=True)
    slot = models.CharField(max_length=200, null=True, blank=True)
    ilvl = models.IntegerField(null=True, blank=True)
    bonus = models.CharField(max_length=200, null=True, blank=True)
    origem = models.CharField(max_length=200, null=True, blank=True)
    identificador = models.CharField(max_length=300)
    wowhead_identificador = models.CharField(max_length=300, null=True, blank=True)
    dropped_by = models.ForeignKey(Boss, related_name='equipamento_dropped_by', null=True, blank=True)
    
    def get_bonus(self):
        bonus = self.bonus.replace("[", "").replace("]", "").replace(" ", "").replace(",", ":")
        return str(bonus)

    def __str__(self):
        return self.nome

    
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

    def compare_gear_last_week(self):
        data_ultima_semana = timezone.now() - datetime.timedelta(weeks=1)
        historico = Historico.objects.filter(personagem = self, data__lt=data_ultima_semana)[:1]

        if (len(historico) == 0):
            historico = Historico.objects.filter(personagem = self).order_by('id')[0]
            #historico = Historico.objects.filter(personagem = p).order_by('-id')[0]

        if ((self.ilvl_equipado - historico.ilvl_equipado) < 0):
            sinal = '-'
        else:
            sinal = '+'

        #historico = Historico.objects.filter(personagem = p, data__lt=data_ultima_semana)[:1]
        return sinal + str(abs(self.ilvl_equipado - historico.ilvl_equipado))
        #return historico.ilvl_equipado

    def get_all_items_wowhead_id(self):
        return set([self.head.wowhead_identificador,  self.shoulder.wowhead_identificador,
                    self.neck.wowhead_identificador,  self.back.wowhead_identificador,
                    self.chest.wowhead_identificador,  self.wrist.wowhead_identificador,
                    self.hands.wowhead_identificador,  self.waist.wowhead_identificador,
                    self.legs.wowhead_identificador,  self.feet.wowhead_identificador,
                    self.finger1.wowhead_identificador,  self.finger2.wowhead_identificador,
                    self.trinket1.wowhead_identificador,  self.trinket2.wowhead_identificador,
                    self.main_hand.wowhead_identificador,  self.off_hand.wowhead_identificador])
    
    def compare_bis(self):
        bis = Bis.objects.get(classe = self.classe, spec = self.spec)
        meus_items =  self.get_all_items_wowhead_id()
        meu_bis = bis.get_all_items_wowhead_id()

        print ('items', meus_items)
        print ('bis', meu_bis)
        return (meus_items & meu_bis)



class Historico(models.Model):
    
    data =  models.DateTimeField(auto_now=True)
    personagem =  models.ForeignKey(Personagem, null=True, blank=True)
    ilvl_equipado = ilvl_equipado = models.IntegerField()


class Bis(models.Model):
    identificador = models.CharField(max_length=200)
    classe = models.CharField(max_length=200, default='1')
    spec = models.CharField(max_length=200, default='1')

    dropped_by = models.ForeignKey(Boss, related_name='bis_dropped_by', null=True, blank=True)

    head = models.ForeignKey(Equipamento, related_name='bis_head', null=True, blank=True)
    shoulder = models.ForeignKey(Equipamento, related_name='bis_shoulder', null=True, blank=True)
    neck = models.ForeignKey(Equipamento, related_name='bis_neck', null=True, blank=True)
    back = models.ForeignKey(Equipamento, related_name='bis_back', null=True, blank=True)
    chest = models.ForeignKey(Equipamento, related_name='bis_chest', null=True, blank=True)
    wrist = models.ForeignKey(Equipamento, related_name='bis_wrist', null=True, blank=True)
    hands = models.ForeignKey(Equipamento, related_name='bis_hands', null=True, blank=True)
    waist = models.ForeignKey(Equipamento, related_name='bis_waist', null=True, blank=True)
    legs = models.ForeignKey(Equipamento, related_name='bis_legs', null=True, blank=True)
    feet = models.ForeignKey(Equipamento, related_name='bis_feet', null=True, blank=True)
    finger1 = models.ForeignKey(Equipamento, related_name='bis_finger1', null=True, blank=True)
    finger2 = models.ForeignKey(Equipamento, related_name='bis_finger2', null=True, blank=True)
    trinket1 = models.ForeignKey(Equipamento, related_name='bis_trinket1', null=True, blank=True)
    trinket2 = models.ForeignKey(Equipamento, related_name='bis_trinket2', null=True, blank=True)
    main_hand = models.ForeignKey(Equipamento, related_name='bis_main_hand', null=True, blank=True)
    off_hand = models.ForeignKey(Equipamento, related_name='bis_off_hand', null=True, blank=True)

    def get_all_items_wowhead_id(self):
        return set([self.head.identificador,  self.shoulder.identificador,
                    self.neck.identificador,  self.back.identificador,
                    self.chest.identificador,  self.wrist.identificador,
                    self.hands.identificador,  self.waist.identificador,
                    self.legs.identificador,  self.feet.identificador,
                    self.finger1.identificador,  self.finger2.identificador,
                    self.trinket1.identificador,  self.trinket2.identificador,
                    self.main_hand.identificador,  self.off_hand.identificador])

    def add_equipment(self, equipamento):
        slot = equipamento.slot
        if slot == 'One-Hand' or slot == 'Two-Hand':
            self.main_hand = equipamento

        elif slot == 'Held In Off-hand' or slot == 'Shield':
            self.off_hand = equipamento

        elif slot == 'Head':
            self.head = equipamento

        elif slot == 'Neck':
            self.neck = equipamento

        elif slot == 'Shoulder':
            self.shoulder = equipamento

        elif slot == 'Cloak':
            self.back = equipamento

        elif slot == 'Robe' or slot == 'Chest':
            self.chest = equipamento

        elif slot == 'Wrist':
            self.wrist = equipamento

        elif slot == 'Hands':
            self.hands = equipamento

        elif slot == 'Waist':
            self.waist = equipamento

        elif slot == 'Legs':
            self.legs = equipamento

        elif slot == 'Feet':
            self.feet = equipamento

        elif slot == 'Finger':
            if self.finger1 == None and self.finger1 != equipamento:
                self.finger1 = equipamento
            if self.finger2 != self.finger1 and self.finger1 != equipamento:
                self.finger2 = equipamento

        elif slot == 'Trinket':
            if self.trinket1 == None and self.trinket1 != equipamento:
                self.trinket1 = equipamento
            if self.trinket2 != self.trinket1 and self.trinket1 != equipamento:
                self.trinket2 = equipamento

        else:
            print ('Item: ' + str(equipamento.nome) + ', slot: ' + str(equipamento.slot) + ' nao foi inserido na BIS!')
            return 'Item: ' + str(equipamento.nome) + ', slot: ' + str(equipamento.slot) + ' nao foi inserido na BIS!'


