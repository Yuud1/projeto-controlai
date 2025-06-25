from django.db import models

class Veiculo(models.Model):
    nome = models.CharField(max_length=100)
    placa = models.CharField(max_length=10)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.placa})"
