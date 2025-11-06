from django.db import models
from django.utils import timezone

# ===================== Categoria de Conta =====================
class CategoriaConta(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

# ===================== Conta =====================
class Conta(models.Model):
    TIPO_CHOICES = [
        ('pagar', 'A Pagar'),
        ('receber', 'A Receber'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('vencido', 'Vencido'),
    ]

    descricao = models.CharField(max_length=200)
    categoria = models.ForeignKey(CategoriaConta, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_vencimento']

    def __str__(self):
        return f"{self.descricao} — {self.get_tipo_display()} — {self.valor}"

    def marcar_pago(self, data_pagamento=None):
        self.data_pagamento = data_pagamento or timezone.now().date()
        self.status = 'pago'
        self.save()

# ===================== Pagamento =====================
# ===================== Pagamento =====================
class Pagamento(models.Model):
    STATUS_CHOICES = [
        ('pago', 'Pago'),
        ('pendente', 'Pendente'),
        ('atrasado', 'Atrasado'),
    ]

    fornecedor = models.CharField(max_length=150, verbose_name="Fornecedor", blank=True, null=True)
    descricao = models.TextField(verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor (R$)")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento", blank=True, null=True)
    data_pagamento = models.DateField(blank=True, null=True, verbose_name="Data de Pagamento")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor} ({self.status})"

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-criado_em']

    # Método para marcar pagamento como pago
    def marcar_pago(self, data_pagamento=None):
        self.data_pagamento = data_pagamento or timezone.now().date()
        self.status = 'pago'
        self.save()


# ===================== Estoque =====================
class ItemEstoque(models.Model):
    CATEGORIA_CHOICES = [
        ('bebidas', 'Bebidas'),
        ('secos', 'Secos'),
        ('molhados', 'Molhados'),
        ('outros', 'Outros'),
    ]

    nome = models.CharField(max_length=150, verbose_name="Nome do Produto")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    quantidade = models.PositiveIntegerField()
    unidade = models.CharField(max_length=20, default='un', verbose_name="Unidade de Medida")
    data_entrada = models.DateField(auto_now_add=True)
    validade = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} - {self.quantidade} {self.unidade}"

    class Meta:
        verbose_name = "Item de Estoque"
        verbose_name_plural = "Itens de Estoque"
        ordering = ['nome']
