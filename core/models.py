import re
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


def normalizar_placa(valor):
    return re.sub(r'[\s-]', '', (valor or '')).upper()


def validar_placa(valor):
    placa = normalizar_placa(valor)
    if not re.fullmatch(r'(?:[A-Z]{3}[0-9]{4}|[A-Z]{3}[0-9][A-Z][0-9]{2})', placa):
        raise ValidationError('Informe uma placa válida, como ABC1234 ou ABC1D23.')


class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=24)
    email = models.EmailField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='veiculos')
    placa = models.CharField(max_length=7, unique=True, db_index=True, validators=[validar_placa])
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    cor = models.CharField(max_length=40, blank=True)
    ano = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['placa']

    def clean(self):
        super().clean()
        self.placa = normalizar_placa(self.placa)
        validar_placa(self.placa)
        if self.ano and not (1900 <= self.ano <= 2100):
            raise ValidationError({'ano': 'Ano fora da faixa permitida.'})

    def save(self, *args, **kwargs):
        self.placa = normalizar_placa(self.placa)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.placa} — {self.marca} {self.modelo}'


class Servico(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='servicos')
    descricao = models.CharField(max_length=180)
    data_servico = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ['-data_servico', '-id']

    def __str__(self):
        return f'{self.descricao} — {self.veiculo.placa}'


class MovimentacaoFinanceira(models.Model):
    RECEITA = 'receita'
    DESPESA = 'despesa'
    TIPOS = [(RECEITA, 'Receita'), (DESPESA, 'Despesa')]
    tipo = models.CharField(max_length=7, choices=TIPOS)
    descricao = models.CharField(max_length=180)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    data_movimentacao = models.DateField()
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, null=True, blank=True, related_name='movimentacoes')

    class Meta:
        ordering = ['-data_movimentacao', '-id']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.descricao}'
