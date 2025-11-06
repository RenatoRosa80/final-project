from django import forms
from .models import Pedido, ItemPedido, Mesa

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['mesa']

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade']
