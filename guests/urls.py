from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),

    # Reservas
    path('salvar-reserva/', views.salvar_reserva, name='salvar_reserva'),
    path('salvar/', views.salvar_reserva, name='salvar'),
    path('confirmacao/', views.confirmacao, name='confirmacao'),
    path('api/fila-espera/', views.api_fila_espera, name='api_fila_espera'),
    path('edite/<int:id>/', views.edite, name='edite'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),

    # Gestão de Mesas (SISTEMA NOVO COMPLETO)
    path('mesas/', views.gerenciar_mesas, name='gerenciar_mesas'),
    path('mesas/adicionar/', views.adicionar_mesa, name='adicionar_mesa'),
    path('mesas/editar/<int:mesa_id>/', views.editar_mesa, name='editar_mesa'),
    path('mesas/excluir/<int:mesa_id>/',
         views.excluir_mesa, name='excluir_mesa'),
    path('mesas/liberar/<int:mesa_id>/',
         views.liberar_mesa, name='liberar_mesa'),
    path('mesas/limpeza/<int:mesa_id>/',
         views.finalizar_limpeza, name='finalizar_limpeza'),
    path('reservas/<int:reserva_id>/atribuir-mesa/',
         views.atribuir_mesa_reserva, name='atribuir_mesa_reserva'),
    path('api/mesas-disponiveis/', views.api_mesas_disponiveis,
         name='api_mesas_disponiveis'),
]
