from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('consulta/', views.consulta, name='consulta'),
    path('historico/<str:placa>/', views.historico, name='historico'),
    path('clientes/novo/', views.cliente_novo, name='cliente_novo'),
    path('veiculos/novo/', views.veiculo_novo, name='veiculo_novo'),
    path('servicos/novo/', views.servico_novo, name='servico_novo'),
    path('financeiro/novo/', views.financeiro_novo, name='financeiro_novo'),
    path('financeiro/', views.financeiro_resumo, name='financeiro_resumo'),
]
