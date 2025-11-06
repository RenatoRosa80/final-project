from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [

    # ======= PÚBLICO (clientes) ======= #
    path('cardapio/', views.cardapio_publico, name='cardapio_publico'),
    path('fazer-pedido/<int:mesa_id>/', views.criar_pedido_cliente, name='criar_pedido_cliente'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),

    # ======= MESAS (staff) ======= #
    path('mesas/', views.lista_mesas, name='lista_mesas'),

    # ======= PEDIDOS (staff) ======= #
    path('pedidos/', views.redirecionar_pedidos, name='lista_pedidos'),  # redireciona para abertos
    path('pedidos/abertos/', views.lista_pedidos_abertos, name='lista_pedidos_abertos'),
    path('pedidos/finalizados/', views.lista_pedidos_finalizados, name='lista_pedidos_finalizados'),

    path('pedidos/nova/', views.criar_pedido_staff, name='criar_pedido'),
    path('pedidos/<int:pedido_id>/', views.detalhes_pedido, name='detalhes_pedido'),
    path('pedidos/<int:pedido_id>/fechar/', views.fechar_pedido, name='fechar_pedido'),

    # ======= ITENS DE PEDIDO ======= #
    path('pedidos/<int:pedido_id>/itens/adicionar/', views.adicionar_item, name='adicionar_item'),
    path('pedidos/itens/<int:item_id>/editar/', views.editar_item, name='editar_item'),
    path('pedidos/itens/<int:item_id>/excluir/', views.excluir_item, name='excluir_item'),
]
