from django.db import models

# Create your models here.

class Guilda(models.Model):
    nome = models.CharField(max_length=200)
    reino = models.CharField(max_length=200)
    identificador = models.CharField(max_length=200)


    def __str__(self):
    	return self.nome + "@" + self.reino
    
class Personagem(models.Model):
    nome = models.CharField(max_length=200)
    ilvl_equipado = models.IntegerField()
    guilda =  models.ForeignKey(Guilda)
    identificador = models.CharField(max_length=200)

    def __str__(self):
    	return self.nome


