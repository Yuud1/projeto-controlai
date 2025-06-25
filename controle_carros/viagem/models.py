from django.db import models
from veiculo.models import Veiculo
from django.contrib.auth.models import User
from datetime import datetime

class Viagem(models.Model):
    STATUS_CHOICES = [
        ('AGENDADA', 'Agendada'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]

    motorista = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='viagens_como_motorista')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    destino = models.CharField(max_length=100)
    data_saida = models.DateTimeField(null=True, blank=True)
    data_retorno = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AGENDADA')
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ['-data_saida']
        verbose_name = 'Viagem'
        verbose_name_plural = 'Viagens'

    def __str__(self):
        return f"{self.destino} - {self.motorista.username if self.motorista else 'Sem motorista'}"

    def save(self, *args, **kwargs):
        # Atualiza a disponibilidade do veículo com base no status da viagem
        if self.status in ['AGENDADA', 'EM_ANDAMENTO']:
            self.veiculo.disponivel = False
        else:
            self.veiculo.disponivel = True
        self.veiculo.save()
        super().save(*args, **kwargs)
