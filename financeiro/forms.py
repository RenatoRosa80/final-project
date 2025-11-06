from django import forms
from .models import Conta, CategoriaConta, Pagamento, ItemEstoque


class CategoriaContaForm(forms.ModelForm):
    class Meta:
        model = CategoriaConta
        fields = ['nome', 'descricao']

class ContaForm(forms.ModelForm):
    data_vencimento = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    data_pagamento = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)

    class Meta:
        model = Conta
        fields = ['descricao', 'categoria', 'tipo', 'valor', 'data_vencimento', 'data_pagamento', 'status', 'observacoes']




class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = '__all__'



class ItemEstoqueForm(forms.ModelForm):
    class Meta:
        model = ItemEstoque
        fields = '__all__'