from django.contrib import admin
from django.urls import path, include
from .views import home, salvar, delete, edite, update

urlpatterns = [
    path('', home),
    path("salvar/", salvar, name = "salvar"),
    path("apagar/<int:id>", delete, name = "delete"),
    path('editar/<int:id>', edite, name = "editar"),
    path('update/<int:id>', update, name = "update"),
]