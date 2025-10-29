from django.db import models


class Mesa(models.Model):
    STATUS_CHOICES = [
        ('livre', 'Livre'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
        ('limpeza', 'Em Limpeza'),
    ]

    numero = models.IntegerField(unique=True, verbose_name="Número da Mesa")
    capacidade = models.IntegerField(verbose_name="Capacidade")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='livre')
    localizacao = models.CharField(
        max_length=100, blank=True, verbose_name="Localização")
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    def __str__(self):
        return f"Mesa {self.numero} ({self.capacidade} pessoas)"

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"


class Reserva(models.Model):
    STATUS_CHOICES = [
        ('espera', 'Em Espera'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('finalizada', 'Finalizada'),
    ]

    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    convidados = models.IntegerField()
    # CORREÇÃO: Removido auto_now_add=True para permitir escolha de data
    data = models.DateField(verbose_name="Data da Reserva")
    # CORREÇÃO: Removido auto_now_add=True para permitir escolha de horário
    horario = models.TimeField(verbose_name="Horário da Reserva")
    solicitacao_especial = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='espera')
    posicao_fila = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Relação com Mesa
    mesa = models.ForeignKey(
        Mesa, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservas')

    def __str__(self):
        return f"Reserva de {self.nome} - {self.data}"

    def save(self, *args, **kwargs):
        # CORREÇÃO: Sintaxe corrigida
        if not self.pk:  # Se for uma nova reserva
            ultima_posicao = Reserva.objects.filter(
                status='espera').order_by('-posicao_fila').first()
            self.posicao_fila = ultima_posicao.posicao_fila + 1 if ultima_posicao else 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
