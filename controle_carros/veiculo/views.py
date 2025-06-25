from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Veiculo

@login_required
def criar_carro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        placa = request.POST.get('placa')
        
        if nome and placa:
            Veiculo.objects.create(
                nome=nome,
                placa=placa.upper(),
                disponivel=True
            )
            messages.success(request, 'Carro cadastrado com sucesso!')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return redirect('dashboard_admin')

@login_required
def editar_carro(request, carro_id):
    carro = get_object_or_404(Veiculo, id=carro_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        placa = request.POST.get('placa')
        disponivel = request.POST.get('disponivel') == 'on'
        
        if nome and placa:
            carro.nome = nome
            carro.placa = placa.upper()
            carro.disponivel = disponivel
            carro.save()
            messages.success(request, 'Carro atualizado com sucesso!')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return redirect('dashboard_admin')

@login_required
def excluir_carro(request, carro_id):
    carro = get_object_or_404(Veiculo, id=carro_id)
    carro.delete()
    messages.success(request, 'Carro excluído com sucesso!')
    return redirect('dashboard_admin')
