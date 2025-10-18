from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    telefone = models.CharField(max_length=30)
    convidados = models.IntegerField(default=10)  # remove max_length
    nascimento = models.DateField()      # remove max_length
    horario = models.TimeField()          # remove max_length
    solicitacao_especial = models.CharField(max_length=1000)


