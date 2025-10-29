from django import forms
from .models import Reserva, Mesa


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidade',
                  'status', 'localizacao', 'observacoes']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'mesa': forms.Select(attrs={'class': 'form-control'}),
            # ... outros widgets ...
        }
