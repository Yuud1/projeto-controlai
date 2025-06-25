from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from veiculo.models import Veiculo
from viagem.models import Viagem
from servico.models import Servico

def index(request):
    return redirect('login')

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect('dashboard_admin')
                else:
                    return redirect('dashboard_usuario')
            else:
                messages.error(request, 'Conta desativada. Entre em contato com o administrador.')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'sistema/login.html')

@never_cache
@login_required
def dashboard_usuario(request):
    return render(request, 'sistema/dashboard_usuario.html')

@login_required
def dashboard_admin(request):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta área.')
        return redirect('dashboard_usuario')

    # Obtém todos os usuários e motoristas
    usuarios = User.objects.all().order_by('username')
    motoristas = User.objects.filter(is_staff=True, is_superuser=False).order_by('username')
    
    # Obtém todos os veículos
    veiculos = Veiculo.objects.all().order_by('nome')
    veiculos_disponiveis = Veiculo.objects.filter(disponivel=True)
    
    # Obtém todas as viagens
    viagens = Viagem.objects.all().order_by('-data_saida')
    viagens_ativas = Viagem.objects.filter(status__in=['AGENDADA', 'EM_ANDAMENTO'])
    
    # Obtém todos os serviços
    servicos = Servico.objects.all().order_by('-data_inicio')
    servicos_ativos = Servico.objects.filter(status__in=['AGENDADO', 'EM_ANDAMENTO'])

    context = {
        'usuarios': usuarios,
        'motoristas': motoristas,
        'veiculos': veiculos,
        'veiculos_disponiveis': veiculos_disponiveis,
        'viagens': viagens,
        'viagens_ativas': viagens_ativas,
        'servicos': servicos,
        'servicos_ativos': servicos_ativos,
        'estatisticas': {
            'total_usuarios': usuarios.count(),
            'total_motoristas': motoristas.count(),
            'total_veiculos': veiculos.count(),
            'veiculos_disponiveis': veiculos_disponiveis.count(),
            'total_viagens': viagens.count(),
            'viagens_ativas': viagens_ativas.count(),
            'total_servicos': servicos.count(),
            'servicos_ativos': servicos_ativos.count(),
        }
    }

    return render(request, 'sistema/dashboard_admin.html', context)

@login_required
def criar_usuario(request):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado. Você não tem permissão para criar usuários.')
        return redirect('dashboard_usuario')

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            tipo_usuario = request.POST.get('tipo_usuario')
            is_active = request.POST.get('is_active') == 'on'
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nome de usuário já existe')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                
                user.is_active = is_active
                if tipo_usuario == 'admin':
                    user.is_superuser = True
                    user.is_staff = True
                elif tipo_usuario == 'motorista':
                    user.is_staff = True
                user.save()
                
                messages.success(request, 'Usuário criado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {str(e)}')
    
    return redirect('dashboard_admin')

@login_required
def editar_usuario(request, usuario_id):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado. Você não tem permissão para editar usuários.')
        return redirect('dashboard_usuario')

    usuario = get_object_or_404(User, id=usuario_id)
    
    if request.method == 'POST':
        try:
            usuario.first_name = request.POST.get('first_name')
            usuario.last_name = request.POST.get('last_name')
            usuario.email = request.POST.get('email')
            usuario.is_active = request.POST.get('is_active') == 'on'
            
            tipo_usuario = request.POST.get('tipo_usuario')
            if tipo_usuario == 'admin':
                usuario.is_superuser = True
                usuario.is_staff = True
            elif tipo_usuario == 'motorista':
                usuario.is_superuser = False
                usuario.is_staff = True
            else:
                usuario.is_superuser = False
                usuario.is_staff = False
            
            if request.POST.get('password'):
                usuario.set_password(request.POST.get('password'))
            
            usuario.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar usuário: {str(e)}')
    
    return redirect('dashboard_admin')

@login_required
def excluir_usuario(request, usuario_id):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado. Você não tem permissão para excluir usuários.')
        return redirect('dashboard_usuario')

    if request.method == 'POST':
        try:
            usuario = get_object_or_404(User, id=usuario_id)
            
            # Impede a exclusão do próprio usuário
            if usuario == request.user:
                messages.error(request, 'Você não pode excluir seu próprio usuário!')
                return redirect('dashboard_admin')
            
            # Verifica se o usuário tem viagens ou serviços ativos
            viagens_ativas = Viagem.objects.filter(motorista=usuario, status__in=['AGENDADA', 'EM_ANDAMENTO']).exists()
            servicos_ativos = Servico.objects.filter(responsavel=usuario, status__in=['AGENDADO', 'EM_ANDAMENTO']).exists()
            
            if viagens_ativas or servicos_ativos:
                messages.error(request, 'Não é possível excluir um usuário com viagens ou serviços ativos!')
                return redirect('dashboard_admin')
            
            usuario.delete()
            messages.success(request, 'Usuário excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir usuário: {str(e)}')
    
    return redirect('dashboard_admin')

def logout_usuario(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema com sucesso!')
    return redirect('login')
