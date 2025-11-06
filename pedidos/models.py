from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from guests.models import Mesa                     # ✅ Mesa do app guests
from estoque.models import Produto                 # ✅ Produto do estoque
from financeiro.models import Pagamento            # ✅ OK


# ============================================================
#  CATEGORIAS DO CARDÁPIO
# ============================================================
class Categoria(models.Model):
    TIPO_CATEGORIA = [
        ('ENTRADA', 'Entradas'),
        ('PRATO', 'Pratos Principais'),
        ('SOBREMESA', 'Sobremesas'),
        ('BEBIDA', 'Bebidas'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CATEGORIA)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


# ============================================================
#  ITENS DO CARDÁPIO
# ============================================================
class ItemCardapio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='itens')
    disponivel = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='cardapio/', blank=True, null=True)
    tempo_preparo = models.PositiveIntegerField(default=15)

    class Meta:
        verbose_name = "Item do Cardápio"
        verbose_name_plural = "Itens do Cardápio"
        ordering = ['categoria', 'nome']

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"


# ============================================================
#  PEDIDOS
# ============================================================
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('finalizado', 'Finalizado'),
    ]
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    aberto = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_abertura']

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa.numero}"

    def calcular_total(self):
        total = sum(item.subtotal() for item in self.itens.all())
        self.valor_total = total
        self.save()
        return total


# ============================================================
#  ITENS DE PEDIDO
# ============================================================
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=True)
    item_cardapio = models.ForeignKey(ItemCardapio, on_delete=models.CASCADE, null=True, blank=True)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Itens de Pedido"

    def __str__(self):
        nome = (
            self.item_cardapio.nome if self.item_cardapio
            else self.produto.nome if self.produto
            else "Item"
        )
        return f"{nome} x {self.quantidade}"

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def save(self, *args, **kwargs):
        # preço automático
        if self.item_cardapio and not self.preco_unitario:
            self.preco_unitario = self.item_cardapio.preco

        if self.produto and not self.preco_unitario:
            self.preco_unitario = self.produto.preco_venda

        super().save(*args, **kwargs)

        # recalcular total do pedido
        if self.pedido:
            self.pedido.calcular_total()
