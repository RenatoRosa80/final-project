from django.db import models
from django.utils import timezone


# ======= CATEGORIAS ======= #
class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoria de Produto"
        verbose_name_plural = "Categorias de Produtos"
        ordering = ['nome']

    def __str__(self):
        return self.nome


# ======= PRODUTOS ======= #
class Produto(models.Model):
    nome = models.CharField(max_length=150)
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.CASCADE, related_name='produtos')
    quantidade = models.PositiveIntegerField(default=0)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_cadastro = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.categoria.nome})"


# ======= MOVIMENTAÇÕES ======= #
class Movimentacao(models.Model):
    TIPOS_MOVIMENTACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    item = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=10, choices=TIPOS_MOVIMENTACAO)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(default=timezone.now)
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.item.nome} ({self.quantidade})"

    def save(self, *args, **kwargs):
        """Atualiza automaticamente a quantidade do produto"""
        if self.pk is None:  # só ajusta na criação
            if self.tipo == 'entrada':
                self.item.quantidade += self.quantidade
            elif self.tipo == 'saida':
                self.item.quantidade -= self.quantidade
            self.item.save()
        super().save(*args, **kwargs)
