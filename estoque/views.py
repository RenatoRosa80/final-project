from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Produto, CategoriaProduto, Movimentacao
from .forms import ProdutoForm, CategoriaProdutoForm, MovimentacaoForm


# ======= RESTRIÇÃO: APENAS STAFF ======= #
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


# ======= DASHBOARD ======= #
@login_required
@staff_required
def dashboard_estoque(request):
    total_produtos = Produto.objects.count()
    total_categorias = CategoriaProduto.objects.count()
    entradas = Movimentacao.objects.filter(tipo='entrada').count()
    saidas = Movimentacao.objects.filter(tipo='saida').count()

    # --- Estatísticas adicionais para o template ---
    estoque_baixo = Produto.objects.filter(quantidade__lt=5)
    bebidas = Produto.objects.filter(categoria__nome__icontains='bebida')
    secos = Produto.objects.filter(categoria__nome__icontains='seco')
    molhados = Produto.objects.filter(categoria__nome__icontains='molhado')
    ultimas_movimentacoes = Movimentacao.objects.order_by('-data')[:10]

    context = {
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'entradas': entradas,
        'saidas': saidas,
        'estoque_baixo': estoque_baixo,
        'bebidas': bebidas,
        'secos': secos,
        'molhados': molhados,
        'ultimas_movimentacoes': ultimas_movimentacoes,
    }
    return render(request, 'estoque/dashboard.html', context)


# ======= PRODUTOS ======= #
@login_required
@staff_required
def lista_produtos(request):
    q = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')

    produtos = Produto.objects.all()
    if q:
        produtos = produtos.filter(Q(nome__icontains=q))
    if categoria:
        produtos = produtos.filter(categoria_id=categoria)

    categorias = CategoriaProduto.objects.all()

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'q': q,
        'categoria': categoria,
    }
    return render(request, 'estoque/lista_produtos.html', context)


@login_required
@staff_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto adicionado com sucesso.')
            return redirect('estoque:lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'estoque/form_produto.html', {'form': form, 'titulo': 'Novo Produto'})


@login_required
@staff_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso.')
            return redirect('estoque:lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'estoque/form_produto.html', {'form': form, 'titulo': f'Editar Produto #{produto.id}'})


@login_required
@staff_required
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto removido com sucesso.')
        return redirect('estoque:lista_produtos')
    return render(request, 'estoque/confirm_excluir.html', {'obj': produto, 'tipo': 'produto'})


# ======= CATEGORIAS ======= #
@login_required
@staff_required
def lista_categorias(request):
    categorias = CategoriaProduto.objects.all()
    return render(request, 'estoque/lista_categorias.html', {'categorias': categorias})


@login_required
@staff_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso.')
            return redirect('estoque:lista_categorias')
    else:
        form = CategoriaProdutoForm()
    return render(request, 'estoque/form_categoria.html', {'form': form})


@login_required
@staff_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(CategoriaProduto, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaProdutoForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso.')
            return redirect('estoque:lista_categorias')
    else:
        form = CategoriaProdutoForm(instance=categoria)
    return render(request, 'estoque/form_categoria.html', {'form': form, 'titulo': 'Editar Categoria'})


@login_required
@staff_required
def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(CategoriaProduto, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso.')
        return redirect('estoque:lista_categorias')
    return render(request, 'estoque/confirm_excluir.html', {'obj': categoria, 'tipo': 'categoria'})


# ======= MOVIMENTAÇÕES ======= #
@login_required
@staff_required
def lista_movimentacoes(request):
    movimentos = Movimentacao.objects.all().order_by('-data')
    return render(request, 'estoque/lista_movimentacoes.html', {'movimentos': movimentos})


@login_required
@staff_required
def criar_movimentacao(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimentação registrada com sucesso.')
            return redirect('estoque:lista_movimentacoes')
    else:
        form = MovimentacaoForm()
    return render(request, 'estoque/form_movimentacao.html', {'form': form, 'titulo': 'Nova Movimentação'})


@login_required
@staff_required
def excluir_movimentacao(request, movimento_id):
    movimento = get_object_or_404(Movimentacao, id=movimento_id)
    if request.method == 'POST':
        movimento.delete()
        messages.success(request, 'Movimentação removida com sucesso.')
        return redirect('estoque:lista_movimentacoes')
    return render(request, 'estoque/confirm_excluir.html', {'obj': movimento, 'tipo': 'movimentação'})
