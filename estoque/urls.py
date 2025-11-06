from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.dashboard_estoque, name='dashboard'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/nova/', views.criar_produto, name='criar_produto'),
    path('produtos/editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('produtos/excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),

    path('movimentacoes/', views.lista_movimentacoes, name='lista_movimentacoes'),
    path('movimentacoes/nova/', views.criar_movimentacao, name='criar_movimentacao'),
]
