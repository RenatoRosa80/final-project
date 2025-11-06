from django import forms
from .models import Produto, CategoriaProduto, Movimentacao


class CategoriaProdutoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProduto
        fields = ['nome', 'descricao']  # campo 'tipo' removido, agora usa 'descricao'


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'categoria',
            'quantidade',
            'preco_custo',
            'preco_venda',
        ]


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = [
            'item',        # corresponde ao Produto
            'tipo',
            'quantidade',
            'observacao',  # corrigido para 'observacao'
        ]
