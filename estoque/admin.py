from django.contrib import admin
from .models import CategoriaProduto, Produto, Movimentacao

# ======= ADMIN CATEGORIA =======
@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

# ======= ADMIN PRODUTO =======
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'quantidade', 'preco_custo', 'preco_venda', 'data_cadastro')
    list_filter = ('categoria',)
    search_fields = ('nome', 'categoria__nome')

# ======= ADMIN MOVIMENTAÇÃO =======
@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('item', 'tipo', 'quantidade', 'data')
    list_filter = ('tipo', 'data')
    search_fields = ('item__nome',)
