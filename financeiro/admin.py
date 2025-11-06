from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Conta, CategoriaConta

@admin.register(CategoriaConta)
class CategoriaContaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo', 'valor', 'data_vencimento', 'status')
    list_filter = ('tipo','status','categoria')
    search_fields = ('descricao','categoria__nome')
