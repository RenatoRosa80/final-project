from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    # ======= CONTAS ======= #
    path('contas/', views.lista_contas, name='lista_contas'),
    path('contas/nova/', views.criar_conta, name='criar_conta'),
    path('contas/editar/<int:conta_id>/', views.editar_conta, name='editar_conta'),
    path('contas/excluir/<int:conta_id>/', views.excluir_conta, name='excluir_conta'),
    path('contas/quitar/<int:conta_id>/', views.quitar_conta, name='quitar_conta'),

    # ======= CATEGORIAS ======= #
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),

    # ======= PAGAMENTOS ======= #
    path('pagamentos/', views.lista_pagamentos, name='lista_pagamentos'),
    path('pagamentos/adicionar/', views.adicionar_pagamento, name='adicionar_pagamento'),
    path('pagamentos/editar/<int:id>/', views.editar_pagamento, name='editar_pagamento'),
    path('pagamentos/excluir/<int:id>/', views.excluir_pagamento, name='excluir_pagamento'),
]
