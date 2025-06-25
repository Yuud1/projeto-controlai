from django.db import models
from veiculo.models import Veiculo
from django.contrib.auth.models import User
from datetime import datetime

class Servico(models.Model):
    TIPO_CHOICES = [
        ('mecanico', 'Mecânico'),
        ('lavagem', 'Lavagem'),
        ('outro', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    custo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AGENDADO')
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-data_inicio']
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.veiculo} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Atualiza a disponibilidade do veículo com base no status do serviço
        if self.status in ['AGENDADO', 'EM_ANDAMENTO']:
            self.veiculo.disponivel = False
        else:
            self.veiculo.disponivel = True
        self.veiculo.save()
        super().save(*args, **kwargs)
