from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from datetime import date

from .models import Conta, CategoriaConta, Pagamento
from .forms import ContaForm, CategoriaContaForm, PagamentoForm


# ====== Restrição de acesso apenas para STAFF ======
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


# ===================== CONTAS =====================

@login_required
@staff_required
def lista_contas(request):
    q = request.GET.get('q', '')
    tipo = request.GET.get('tipo', '')
    status = request.GET.get('status', '')
    contas = Conta.objects.all()

    if q:
        contas = contas.filter(Q(descricao__icontains=q) | Q(categoria__nome__icontains=q))
    if tipo:
        contas = contas.filter(tipo=tipo)
    if status:
        contas = contas.filter(status=status)

    hoje = date.today()
    contas_vencidas = contas.filter(status='pendente', data_vencimento__lt=hoje)

    context = {
        'contas': contas,
        'q': q,
        'tipo': tipo,
        'status': status,
        'contas_vencidas': contas_vencidas,
    }
    return render(request, 'financeiro/lista_contas.html', context)


@login_required
@staff_required
def criar_conta(request):
    if request.method == 'POST':
        form = ContaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso.')
            return redirect('financeiro:lista_contas')
    else:
        form = ContaForm()
    return render(request, 'financeiro/form_conta.html', {'form': form, 'titulo': 'Nova Conta'})


@login_required
@staff_required
def editar_conta(request, conta_id):
    conta = get_object_or_404(Conta, id=conta_id)
    if request.method == 'POST':
        form = ContaForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta atualizada com sucesso.')
            return redirect('financeiro:lista_contas')
    else:
        form = ContaForm(instance=conta)
    return render(request, 'financeiro/form_conta.html', {'form': form, 'titulo': f'Editar Conta #{conta.id}'})


@login_required
@staff_required
def excluir_conta(request, conta_id):
    conta = get_object_or_404(Conta, id=conta_id)
    if request.method == 'POST':
        conta.delete()
        messages.success(request, 'Conta excluída com sucesso.')
        return redirect('financeiro:lista_contas')
    return render(request, 'financeiro/confirm_excluir.html', {'obj': conta, 'tipo': 'conta'})


@login_required
@staff_required
def quitar_conta(request, conta_id):
    conta = get_object_or_404(Conta, id=conta_id)
    if request.method == 'POST':
        conta.marcar_pago()
        messages.success(request, 'Conta marcada como paga.')
    return redirect('financeiro:lista_contas')


# ===================== CATEGORIAS =====================

@login_required
@staff_required
def lista_categorias(request):
    categorias = CategoriaConta.objects.all()
    return render(request, 'financeiro/lista_categorias.html', {'categorias': categorias})


@login_required
@staff_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaContaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso.')
            return redirect('financeiro:lista_categorias')
    else:
        form = CategoriaContaForm()
    return render(request, 'financeiro/form_categoria.html', {'form': form})


# ===================== PAGAMENTOS =====================

@login_required
@staff_required
def lista_pagamentos(request):
    pagamentos = Pagamento.objects.all().order_by('-data_vencimento')
    return render(request, 'financeiro/lista_pagamentos.html', {'pagamentos': pagamentos})


@login_required
@staff_required
def adicionar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pagamento adicionado com sucesso.")
            return redirect('financeiro:lista_pagamentos')
    else:
        form = PagamentoForm()
    return render(request, 'financeiro/form_pagamento.html', {'form': form, 'titulo': 'Novo Pagamento'})


@login_required
@staff_required
def editar_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, id=id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Pagamento atualizado com sucesso.")
            return redirect('financeiro:lista_pagamentos')
    else:
        form = PagamentoForm(instance=pagamento)
    return render(request, 'financeiro/form_pagamento.html', {'form': form, 'titulo': 'Editar Pagamento'})


@login_required
@staff_required
def excluir_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, id=id)
    if request.method == 'POST':
        pagamento.delete()
        messages.success(request, "Pagamento excluído com sucesso.")
        return redirect('financeiro:lista_pagamentos')
    return render(request, 'financeiro/confirm_excluir.html', {'obj': pagamento, 'tipo': 'pagamento'})
