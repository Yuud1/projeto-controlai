# Generated by Django 5.2.3 on 2025-06-25 02:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servico',
            options={'ordering': ['-data_inicio'], 'verbose_name': 'Serviço', 'verbose_name_plural': 'Serviços'},
        ),
        migrations.AddField(
            model_name='servico',
            name='custo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='servico',
            name='status',
            field=models.CharField(choices=[('AGENDADO', 'Agendado'), ('EM_ANDAMENTO', 'Em Andamento'), ('CONCLUIDO', 'Concluído'), ('CANCELADO', 'Cancelado')], default='AGENDADO', max_length=20),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_fim',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateTimeField(),
        ),
    ]
