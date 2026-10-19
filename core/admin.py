from django.contrib import admin
from .models import Cliente, Veiculo, Servico, MovimentacaoFinanceira

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'data_cadastro')
    search_fields = ('nome', 'telefone')

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'cliente')
    search_fields = ('placa', 'cliente__nome')

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'veiculo', 'data_servico', 'valor')
    search_fields = ('veiculo__placa', 'descricao')

@admin.register(MovimentacaoFinanceira)
class MovimentacaoFinanceiraAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descricao', 'valor', 'data_movimentacao')
