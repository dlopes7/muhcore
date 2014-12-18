from django.db import models

# Create your models here.

class Guilda(models.Model):
    nome = models.CharField(max_length=200)
    reino = models.CharField(max_length=200)
    identificador = models.CharField(max_length=200)


    def __str__(self):
    	return self.nome + "@" + self.reino

class Equipamento(models.Model):
	nome = models.CharField(max_length=200)
    origem = models.CharField(max_length=200)
	slot = models.CharField(max_length=200)
	ilvl = models.IntegerField()
	identificador = models.IntegerField(primary_key=True)
	def __str__(self):
		return self.nome

class Personagem(models.Model):
    nome = models.CharField(max_length=200)
    ilvl_equipado = models.IntegerField()
    identificador = models.CharField(max_length=200)
    guilda =  models.ForeignKey(Guilda, related_name='personagem_guilda')
    head = models.ForeignKey(Equipamento, related_name='personagem_head')
    shoulder = models.ForeignKey(Equipamento, related_name='personagem_shoulder')
    back = models.ForeignKey(Equipamento, related_name='personagem_back')
    chest = models.ForeignKey(Equipamento, related_name='personagem_chest')
    wrist = models.ForeignKey(Equipamento, related_name='personagem_wrist')
    hands = models.ForeignKey(Equipamento, related_name='personagem_hands')
    waist = models.ForeignKey(Equipamento, related_name='personagem_waist')
    legs = models.ForeignKey(Equipamento, related_name='personagem_legs')
    feet = models.ForeignKey(Equipamento, related_name='personagem_feet')
    finger1 = models.ForeignKey(Equipamento, related_name='personagem_finger1')
    finger2 = models.ForeignKey(Equipamento, related_name='personagem_finger2')
    trinket1 = models.ForeignKey(Equipamento, related_name='personagem_trinket1')
    trinket2 = models.ForeignKey(Equipamento, related_name='personagem_trinket2')
    main_hand = models.ForeignKey(Equipamento, related_name='personagem_main_hand')
    off_hand = models.ForeignKey(Equipamento, related_name='personagem_off_hand')


    def __str__(self):
    	return self.nome


