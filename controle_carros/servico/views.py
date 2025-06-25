from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Servico
from veiculo.models import Veiculo
from django.contrib.auth.models import User
from datetime import datetime

@login_required
def novo_servico(request):
    if request.method == 'POST':
        try:
            veiculo = Veiculo.objects.get(id=request.POST.get('veiculo'))
            responsavel = request.user
            
            servico = Servico.objects.create(
                veiculo=veiculo,
                tipo=request.POST.get('tipo'),
                descricao=request.POST.get('descricao', ''),
                data_inicio=request.POST.get('data_inicio'),
                data_fim=request.POST.get('data_fim'),
                custo=request.POST.get('custo', 0.00),
                status='AGENDADO',
                responsavel=responsavel
            )
            
            messages.success(request, 'Serviço criado com sucesso!')
            return redirect('dashboard_admin')
        except Exception as e:
            messages.error(request, f'Erro ao criar serviço: {str(e)}')
            return redirect('dashboard_admin')
    return redirect('dashboard_admin')

@login_required
def editar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    
    if request.method == 'POST':
        try:
            veiculo = Veiculo.objects.get(id=request.POST.get('veiculo'))
            
            servico.veiculo = veiculo
            servico.tipo = request.POST.get('tipo')
            servico.descricao = request.POST.get('descricao', '')
            servico.data_inicio = request.POST.get('data_inicio')
            servico.data_fim = request.POST.get('data_fim')
            servico.custo = request.POST.get('custo', servico.custo)
            servico.status = request.POST.get('status')
            
            servico.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar serviço: {str(e)}')
    
    return redirect('dashboard_admin')

@login_required
def excluir_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    
    if request.method == 'POST':
        try:
            # Verifica se o serviço está em andamento
            if servico.status == 'EM_ANDAMENTO':
                messages.error(request, 'Não é possível excluir um serviço em andamento!')
                return redirect('dashboard_admin')
                
            servico.delete()
            messages.success(request, 'Serviço excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir serviço: {str(e)}')
    
    return redirect('dashboard_admin')
