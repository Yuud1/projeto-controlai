from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Viagem
from veiculo.models import Veiculo
from django.contrib.auth.models import User
from datetime import datetime

@login_required
def nova_viagem(request):
    if request.method == 'POST':
        try:
            motorista = User.objects.get(id=request.POST.get('motorista'))
            veiculo = Veiculo.objects.get(id=request.POST.get('veiculo'))
            
            viagem = Viagem.objects.create(
                motorista=motorista,
                veiculo=veiculo,
                destino=request.POST.get('destino'),
                data_saida=request.POST.get('data_saida'),
                data_retorno=request.POST.get('data_retorno')
            )
            
            messages.success(request, 'Viagem criada com sucesso!')
            return redirect('dashboard_admin')
        except Exception as e:
            messages.error(request, f'Erro ao criar viagem: {str(e)}')
            return redirect('dashboard_admin')
    return redirect('dashboard_admin')

@login_required
def editar_viagem(request, viagem_id):
    viagem = get_object_or_404(Viagem, id=viagem_id)
    
    if request.method == 'POST':
        try:
            motorista = User.objects.get(id=request.POST.get('motorista'))
            veiculo = Veiculo.objects.get(id=request.POST.get('veiculo'))
            
            viagem.motorista = motorista
            viagem.veiculo = veiculo
            viagem.destino = request.POST.get('destino')
            viagem.data_saida = request.POST.get('data_saida')
            viagem.data_retorno = request.POST.get('data_retorno')
            viagem.status = request.POST.get('status')
            
            viagem.save()
            messages.success(request, 'Viagem atualizada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar viagem: {str(e)}')
    
    return redirect('dashboard_admin')

@login_required
def excluir_viagem(request, viagem_id):
    viagem = get_object_or_404(Viagem, id=viagem_id)
    
    if request.method == 'POST':
        try:
            viagem.delete()
            messages.success(request, 'Viagem excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir viagem: {str(e)}')
    
    return redirect('dashboard_admin')
