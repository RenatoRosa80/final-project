from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone

from guests.models import Mesa
from .models import Pedido, ItemPedido, Categoria, ItemCardapio
from .forms import PedidoForm, ItemPedidoForm
from financeiro.models import Pagamento


# ================================
#   PERMISSÃO STAFF
# ================================
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


# ================================
#   CARDÁPIO PÚBLICO (CLIENTE)
# ================================
def cardapio_publico(request):
    categorias = Categoria.objects.prefetch_related('itens').all()
    mesas = Mesa.objects.filter(status='ocupada').order_by('numero')  # ✅ somente ocupadas
    return render(request, 'pedidos/cardapio_publico.html', {
        'categorias': categorias,
        'mesas': mesas
    })


# ================================
#   CRIAR PEDIDO – CLIENTE
# ================================
@login_required
def criar_pedido_cliente(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id, status='ocupada')

    # ✅ Impedir mais de um pedido aberto na mesa
    pedido_aberto = Pedido.objects.filter(mesa=mesa, aberto=True).first()
    if pedido_aberto:
        messages.warning(request, f"Já existe o Pedido #{pedido_aberto.id} aberto na mesa {mesa.numero}.")
        return redirect('pedidos:detalhes_pedido', pedido_aberto.id)

    if request.method == "POST":
        pedido = Pedido.objects.create(
            mesa=mesa,
            cliente=request.user,
            aberto=True,
            data_abertura=timezone.now()
        )

        itens = request.POST.getlist('itens')
        quantidades = request.POST.getlist('quantidades')

        for item_id, quantidade in zip(itens, quantidades):
            try:
                qtd = int(quantidade or 0)
            except:
                qtd = 0

            if qtd > 0:
                card = get_object_or_404(ItemCardapio, id=item_id, disponivel=True)
                ItemPedido.objects.create(
                    pedido=pedido,
                    item_cardapio=card,
                    quantidade=qtd,
                    preco_unitario=card.preco
                )

        pedido.calcular_total()
        messages.success(request, f"Pedido #{pedido.id} criado com sucesso!")
        return redirect('pedidos:detalhes_pedido', pedido.id)

    categorias = Categoria.objects.prefetch_related('itens').all()
    return render(request, 'pedidos/criar_pedido_cliente.html', {
        'mesa': mesa,
        'categorias': categorias
    })


# ================================
#   MEUS PEDIDOS (CLIENTE)
# ================================
@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-data_abertura')
    return render(request, 'pedidos/meus_pedidos.html', {'pedidos': pedidos})


# ================================
#   MESAS (STAFF)
# ================================
@login_required
@staff_required
def lista_mesas(request):
    mesas = Mesa.objects.all().order_by('numero')
    return render(request, 'pedidos/lista_mesas.html', {'mesas': mesas})


# ================================
#   LISTA PEDIDOS (STAFF)
# ================================
@login_required
@staff_required
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-id')
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})


# ================================
#   CRIAR PEDIDO – STAFF
# ================================
@login_required
@staff_required
def criar_pedido_staff(request):
    mesa_id = request.GET.get('mesa')
    form = PedidoForm(initial={'mesa': mesa_id} if mesa_id else None)

    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.aberto = True
            pedido.data_abertura = timezone.now()
            pedido.save()

            messages.success(request, f"Pedido #{pedido.id} criado com sucesso!")
            return redirect('pedidos:detalhes_pedido', pedido.id)

    return render(request, 'pedidos/form_pedido.html', {
        'form': form,
        'titulo': 'Novo Pedido'
    })


# ================================
#   DETALHES DO PEDIDO
# ================================
@login_required
@staff_required
def detalhes_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    itens = pedido.itens.all()
    total = sum(i.subtotal() for i in itens)

    pedido.valor_total = total
    pedido.save()

    return render(request, 'pedidos/detalhes_pedido.html', {
        'pedido': pedido,
        'itens': itens,
        'total': total,
    })


# ================================
#   ADICIONAR ITEM (STAFF)
# ================================
@login_required
@staff_required
def adicionar_item(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    form = ItemPedidoForm()

    if request.method == "POST":
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido
            if item.item_cardapio:
                item.preco_unitario = item.item_cardapio.preco
            item.save()

            messages.success(request, "Item adicionado ao pedido!")
            return redirect('pedidos:detalhes_pedido', pedido_id)

    return render(request, 'pedidos/form_item_pedido.html', {
        'form': form,
        'pedido': pedido
    })


# ================================
#   EDITAR ITEM (STAFF)
# ================================
@login_required
@staff_required
def editar_item(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id)
    form = ItemPedidoForm(instance=item)

    if request.method == "POST":
        form = ItemPedidoForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            if item.item_cardapio:
                item.preco_unitario = item.item_cardapio.preco
            item.save()

            messages.success(request, "Item atualizado!")
            return redirect('pedidos:detalhes_pedido', item.pedido.id)

    return render(request, 'pedidos/form_item_pedido.html', {
        'form': form,
        'pedido': item.pedido
    })


# ================================
#   EXCLUIR ITEM (STAFF)
# ================================
@login_required
@staff_required
def excluir_item(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id)

    if request.method == "POST":
        pedido_id = item.pedido.id
        item.delete()
        messages.success(request, "Item removido com sucesso!")
        return redirect('pedidos:detalhes_pedido', pedido_id)

    return render(request, 'pedidos/confirm_excluir_item.html', {
        'item': item,
        'pedido': item.pedido
    })


# ================================
#   FECHAR PEDIDO (STAFF)
# ================================
@login_required
@staff_required
def fechar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == "POST":
        # Fecha o pedido
        pedido.aberto = False
        pedido.status = 'finalizado'
        pedido.data_fechamento = timezone.now()
        pedido.save()

        # Atualiza mesa
        mesa = pedido.mesa
        mesa.status = 'limpeza'
        mesa.save()

        # Gera pagamento pendente
        Pagamento.objects.create(
            descricao=f"Pagamento Pedido #{pedido.id} – Mesa {mesa.numero}",
            valor=pedido.valor_total,
            status='pendente'
        )

        messages.success(request, f"Pedido #{pedido.id} finalizado e mesa {mesa.numero} enviada para limpeza.")
        return redirect('pedidos:lista_pedidos_abertos')

    return render(request, 'pedidos/confirm_fechar_pedido.html', {
        'pedido': pedido,
        'total': pedido.valor_total
    })


# ================================
#   LISTAS DE PEDIDOS (STAFF)
# ================================
@login_required
@staff_required
def lista_pedidos_abertos(request):
    pedidos = Pedido.objects.filter(aberto=True).select_related('mesa', 'cliente').order_by('-id')
    return render(request, 'pedidos/lista_pedidos.html', {
        'pedidos': pedidos,
        'titulo': 'Pedidos Abertos',
        'tipo_lista': 'abertos'
    })


@login_required
@staff_required
def lista_pedidos_finalizados(request):
    pedidos = Pedido.objects.filter(aberto=False).select_related('mesa', 'cliente').order_by('-data_fechamento')
    return render(request, 'pedidos/lista_pedidos.html', {
        'pedidos': pedidos,
        'titulo': 'Pedidos Finalizados',
        'tipo_lista': 'finalizados'
    })


# ================================
#   HOME DE PEDIDOS (Redireciona)
# ================================
@login_required
@staff_required
def pedidos_home(request):
    """Redireciona /pedidos/ para a lista de abertos"""
    return redirect('pedidos:lista_pedidos_abertos')


# ================================
#   REDIRECIONAR /PEDIDOS → ABERTOS
# ================================
from django.shortcuts import redirect

@login_required
@staff_required
def redirecionar_pedidos(request):
    """
    Redireciona a rota /pedidos/ para a lista de pedidos abertos.
    """
    return redirect('pedidos:lista_pedidos_abertos')
