# IMPORTS PRIMEIRO - ANTES DE QUALQUER CÓDIGO
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from collections import defaultdict
from datetime import datetime, date
from .models import Reserva, Mesa
from .forms import MesaForm
from django.db.models import Q

# FUNÇÃO HOME (Página inicial)


def home(request):
    """Página inicial do sistema de reservas"""
    try:
        reservas_em_espera = Reserva.objects.filter(
            status='espera').order_by('posicao_fila')[:5]
        total_na_fila = Reserva.objects.filter(status='espera').count()
    except Exception as e:
        reservas_em_espera = []
        total_na_fila = 0
        print(f"Erro ao carregar reservas: {e}")

    return render(request, 'index.html', {
        'ultimas_reservas': reservas_em_espera,
        'total_na_fila': total_na_fila
    })

# FUNÇÃO SALVAR RESERVA


def salvar_reserva(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            idade = request.POST.get('idade')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            convidados = request.POST.get('convidados')
            # CORREÇÃO: Capturar data e horário do formulário
            data_reserva = request.POST.get('dia')
            horario_reserva = request.POST.get('horario')
            solicitacao_especial = request.POST.get('solicitacao_especial', '')

            # Validação básica
            if not all([nome, idade, email, telefone, convidados, data_reserva, horario_reserva]):
                messages.error(
                    request, 'Todos os campos obrigatórios devem ser preenchidos.')
                return redirect('/#book-a-table')

            # Cria a reserva com data e horário fornecidos
            reserva = Reserva(
                nome=nome,
                idade=idade,
                email=email,
                telefone=telefone,
                convidados=convidados,
                data=data_reserva,  # CORREÇÃO: Usar data do formulário
                horario=horario_reserva,  # CORREÇÃO: Usar horário do formulário
                solicitacao_especial=solicitacao_especial
            )

            reserva.save()

            messages.success(
                request, f'Reserva cadastrada com sucesso! Sua posição na fila é: {reserva.posicao_fila}')
            return redirect('/#book-a-table')

        except Exception as e:
            messages.error(request, f'Erro ao salvar reserva: {str(e)}')
            return redirect('/#book-a-table')

    return redirect('/#book-a-table')

# FUNÇÃO SALVAR (alias)


def salvar(request):
    return salvar_reserva(request)

# FUNÇÃO CONFIRMAÇÃO


def confirmacao(request):
    try:
        ultima_reserva = Reserva.objects.last()
        reservas_em_espera = Reserva.objects.filter(
            status='espera').order_by('posicao_fila')
        total_na_fila = reservas_em_espera.count()
    except:
        ultima_reserva = None
        reservas_em_espera = []
        total_na_fila = 0

    return render(request, 'confirmacao_reserva.html', {
        'reserva': ultima_reserva,
        'fila_espera': reservas_em_espera,
        'total_na_fila': total_na_fila,
    })

# FUNÇÃO LISTA RESERVAS (COM FILTRO CORRIGIDO)


@login_required
def lista_reservas(request):
    try:
        # Obter o parâmetro de filtro primeiro
        data_filtro = request.GET.get('data')

        # Se há filtro, buscar apenas as reservas da data específica
        if data_filtro:
            try:
                # Converter a string para objeto date
                data_obj = datetime.strptime(data_filtro, '%Y-%m-%d').date()
                reservas = Reserva.objects.filter(
                    data=data_obj).order_by('horario')

                # Para modo filtrado, ainda precisamos agrupar por data
                reservas_agrupadas = [{
                    'data': data_obj,
                    'reservas': reservas
                }]

            except ValueError:
                messages.error(request, 'Data inválida para filtro.')
                reservas = Reserva.objects.all().order_by('data', 'horario')
                data_filtro = None
        else:
            # Modo normal - todas as reservas agrupadas por data
            reservas = Reserva.objects.all().order_by('data', 'horario')

            # Agrupar reservas por data
            reservas_por_dia = {}
            for reserva in reservas:
                if reserva.data not in reservas_por_dia:
                    reservas_por_dia[reserva.data] = []
                reservas_por_dia[reserva.data].append(reserva)

            # Converter para lista ordenada
            reservas_agrupadas = []
            for data in sorted(reservas_por_dia.keys()):
                reservas_agrupadas.append({
                    'data': data,
                    'reservas': reservas_por_dia[data]
                })

        # Estatísticas (sempre baseadas nas reservas atuais)
        total_reservas = reservas.count()
        reservas_espera = reservas.filter(status='espera').count()
        reservas_confirmadas = reservas.filter(status='confirmada').count()
        total_convidados = sum(reserva.convidados for reserva in reservas)

        # Mesas disponíveis
        mesas_disponiveis = Mesa.objects.all().order_by('numero')

        context = {
            'reservas_agrupadas': reservas_agrupadas,
            'reservas': reservas,
            'total_reservas': total_reservas,
            'reservas_espera': reservas_espera,
            'reservas_confirmadas': reservas_confirmadas,
            'total_convidados': total_convidados,
            'data_filtro': data_filtro,
            'hoje': date.today(),
            'mesas_disponiveis': mesas_disponiveis,
        }

    except Exception as e:
        messages.error(request, f'Erro ao carregar reservas: {str(e)}')
        context = {
            'reservas_agrupadas': [],
            'reservas': [],
            'total_reservas': 0,
            'reservas_espera': 0,
            'reservas_confirmadas': 0,
            'total_convidados': 0,
            'data_filtro': None,
            'hoje': date.today(),
            'mesas_disponiveis': [],
        }

    return render(request, 'lista_reservas.html', context)

# FUNÇÃO LISTA (alias)


def lista_reserva(request):
    return lista_reservas(request)

# FUNÇÃO API FILA DE ESPERA


def api_fila_espera(request):
    try:
        reservas = Reserva.objects.filter(
            status='espera').order_by('posicao_fila')[:10]
        data = {
            'reservas': list(reservas.values('nome', 'convidados', 'posicao_fila'))
        }
    except:
        data = {'reservas': []}

    return JsonResponse(data)

# FUNÇÃO UPDATE


@login_required
def update(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if request.method == 'POST':
        try:
            reserva.nome = request.POST.get('nome')
            reserva.idade = request.POST.get('idade')
            reserva.email = request.POST.get('email')
            reserva.telefone = request.POST.get('telefone')
            reserva.convidados = request.POST.get('convidados')
            # CORREÇÃO: Capturar data e horário
            reserva.data = request.POST.get('data')
            reserva.horario = request.POST.get('horario')
            reserva.solicitacao_especial = request.POST.get(
                'solicitacao_especial', '')
            reserva.status = request.POST.get('status', 'espera')

            reserva.save()
            messages.success(request, 'Reserva atualizada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar reserva: {str(e)}')

        return redirect('lista_reservas')

    return render(request, 'editar_reservas.html', {'reserva': reserva})

# FUNÇÃO DELETE


@login_required
def delete(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    try:
        reserva.delete()
        messages.success(request, 'Reserva excluída com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir reserva: {str(e)}')

    return redirect('lista_reservas')

# FUNÇÃO EDITE


@login_required
def edite(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    return render(request, 'editar_reservas.html', {'reserva': reserva})

# FUNÇÃO LOGIN


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('lista_reservas')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'registration/login.html')

# FUNÇÃO LOGOUT


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')

# FUNÇÃO ADMIN DASHBOARD


@login_required
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('lista_reservas')

# GESTÃO DE MESAS

@login_required
def gerenciar_mesas(request):
    """Visualização principal do gerenciamento de mesas"""
    mesas = Mesa.objects.all().order_by('numero')

    # Estatísticas CORRETAS
    mesas_livres = mesas.filter(status='livre').count()
    mesas_ocupadas = mesas.filter(status='ocupada').count()
    mesas_reservadas = mesas.filter(status='reservada').count()
    mesas_limpeza = mesas.filter(status='limpeza').count()

    context = {
        'mesas': mesas,
        'mesas_livres': mesas_livres,
        'mesas_ocupadas': mesas_ocupadas,
        'mesas_reservadas': mesas_reservadas,
        'mesas_limpeza': mesas_limpeza,
        'total_mesas': mesas.count(),
    }
    return render(request, 'gerenciar_mesas.html', context)


@login_required
def adicionar_mesa(request):
    """Adicionar nova mesa"""
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesa adicionada com sucesso!')
            return redirect('gerenciar_mesas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = MesaForm()

    # CORREÇÃO: Usar template existente
    return render(request, 'form_mesa.html', {'form': form, 'mesa': None})


@login_required
def editar_mesa(request, mesa_id):
    """Editar mesa existente"""
    mesa = get_object_or_404(Mesa, id=mesa_id)

    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            mesa_salva = form.save()
            messages.success(
                request, f'Mesa {mesa_salva.numero} atualizada com sucesso!')
            return redirect('gerenciar_mesas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = MesaForm(instance=mesa)

    context = {
        'form': form,
        'mesa': mesa
    }

    # ✅ CORREÇÃO: Usar o template correto que já existe
    return render(request, 'form_mesa.html', context)


@login_required
def excluir_mesa(request, mesa_id):
    """Excluir mesa"""
    mesa = get_object_or_404(Mesa, id=mesa_id)

    # Verificar se a mesa tem reservas ativas
    reservas_ativas = mesa.reservas.filter(
        Q(status='confirmada') | Q(status='espera')
    ).exists()

    if reservas_ativas:
        messages.error(
            request, 'Não é possível excluir uma mesa com reservas ativas!')
    else:
        mesa.delete()
        messages.success(request, 'Mesa excluída com sucesso!')

    return redirect('gerenciar_mesas')


@login_required
def atribuir_mesa_reserva(request, reserva_id):
    """Atribuir mesa a uma reserva"""
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        mesa_id = request.POST.get('mesa_id')

        if mesa_id:
            mesa = get_object_or_404(Mesa, id=mesa_id)

            # Verificar se a mesa está disponível
            if mesa.status == 'livre' or (reserva.mesa and reserva.mesa.id == mesa.id):
                # Liberar mesa anterior se houver (e não for a mesma mesa)
                if reserva.mesa and reserva.mesa.id != mesa.id:
                    mesa_anterior = reserva.mesa
                    mesa_anterior.status = 'livre'
                    mesa_anterior.save()

                # Atribuir nova mesa
                reserva.mesa = mesa
                reserva.status = 'confirmada'
                mesa.status = 'reservada'

                reserva.save()
                mesa.save()

                messages.success(
                    request, f'Mesa {mesa.numero} atribuída à reserva!')
            else:
                messages.error(request, 'Mesa não está disponível!')
        else:
            # Remover mesa da reserva
            if reserva.mesa:
                mesa_anterior = reserva.mesa
                mesa_anterior.status = 'livre'
                mesa_anterior.save()
                reserva.mesa = None
                reserva.status = 'espera'  # Voltar para espera se remover a mesa
                reserva.save()
                messages.success(request, 'Mesa removida da reserva!')

    return redirect('lista_reservas')


@login_required
def liberar_mesa(request, mesa_id):
    """Liberar mesa (após pagamento/fim do uso)"""
    mesa = get_object_or_404(Mesa, id=mesa_id)

    # Encontrar reserva ativa para esta mesa
    reserva_ativa = mesa.reservas.filter(
        Q(status='confirmada') | Q(status='espera')
    ).first()

    if reserva_ativa:
        reserva_ativa.mesa = None
        reserva_ativa.status = 'finalizada'
        reserva_ativa.save()

    mesa.status = 'limpeza'
    mesa.save()

    messages.success(request, f'Mesa {mesa.numero} liberada para limpeza!')
    return redirect('gerenciar_mesas')


@login_required
def finalizar_limpeza(request, mesa_id):
    """Finalizar limpeza e deixar mesa livre"""
    mesa = get_object_or_404(Mesa, id=mesa_id)

    if mesa.status == 'limpeza':
        mesa.status = 'livre'
        mesa.save()
        messages.success(request, f'Mesa {mesa.numero} está livre!')
    else:
        messages.error(request, 'A mesa não está em processo de limpeza!')

    return redirect('gerenciar_mesas')


@login_required
def api_mesas_disponiveis(request):
    """API para obter mesas disponíveis para uma reserva"""
    data_reserva = request.GET.get('data')
    horario_reserva = request.GET.get('horario')
    convidados = int(request.GET.get('convidados', 1))

    # Mesas livres com capacidade suficiente
    mesas_disponiveis = Mesa.objects.filter(
        status='livre',
        capacidade__gte=convidados
    ).values('id', 'numero', 'capacidade', 'localizacao')

    return JsonResponse(list(mesas_disponiveis), safe=False)
