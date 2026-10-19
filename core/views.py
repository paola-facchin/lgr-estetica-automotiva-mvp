from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import ClienteForm, VeiculoForm, ServicoForm, FinanceiroForm, PlacaForm
from .models import Veiculo, MovimentacaoFinanceira

@login_required
def inicio(request):
    return render(request, 'core/inicio.html')

@login_required
def consulta(request):
    form = PlacaForm(request.GET or None)
    if 'placa' in request.GET and form.is_valid():
        return redirect('historico', placa=form.cleaned_data['placa'])
    return render(request, 'core/consulta.html', {'form': form})

@login_required
def historico(request, placa):
    form = PlacaForm({'placa': placa})
    if not form.is_valid():
        messages.error(request, 'Placa inválida. Confira os 7 caracteres e tente novamente.')
        return redirect('consulta')
    veiculo = Veiculo.objects.select_related('cliente').filter(placa=form.cleaned_data['placa']).first()
    servicos = veiculo.servicos.all() if veiculo else []
    return render(request, 'core/historico.html', {'veiculo': veiculo, 'servicos': servicos, 'placa': form.cleaned_data['placa']})

@login_required
def cliente_novo(request):
    return _criar(request, ClienteForm, 'Cliente cadastrado.', 'Novo cliente')

@login_required
def veiculo_novo(request):
    return _criar(request, VeiculoForm, 'Veículo cadastrado.', 'Novo veículo')

@login_required
def servico_novo(request):
    return _criar(request, ServicoForm, 'Serviço registrado.', 'Novo serviço')

@permission_required('core.add_movimentacaofinanceira', raise_exception=True)
def financeiro_novo(request):
    return _criar(request, FinanceiroForm, 'Movimentação registrada.', 'Nova movimentação')

@login_required
def _criar(request, form_class, msg, titulo):
    form = form_class(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, msg)
        return redirect('inicio')
    return render(request, 'core/formulario.html', {'form': form, 'titulo': titulo})

@permission_required('core.view_movimentacaofinanceira', raise_exception=True)
def financeiro_resumo(request):
    filtro = {}
    data_inicial = request.GET.get('inicio', '')
    data_final = request.GET.get('fim', '')
    # Apenas datas no formato ISO são aceitas.
    from datetime import date
    try:
        if data_inicial:
            filtro['data_movimentacao__gte'] = date.fromisoformat(data_inicial)
        if data_final:
            filtro['data_movimentacao__lte'] = date.fromisoformat(data_final)
    except ValueError:
        messages.error(request, 'Informe datas válidas no formato AAAA-MM-DD.')
        filtro = {'pk__in': []}
    qs = MovimentacaoFinanceira.objects.filter(**filtro)
    receitas = qs.filter(tipo=MovimentacaoFinanceira.RECEITA).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    despesas = qs.filter(tipo=MovimentacaoFinanceira.DESPESA).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    return render(request, 'core/financeiro.html', {
        'receitas': receitas, 'despesas': despesas, 'saldo': receitas - despesas,
        'movimentacoes': qs[:100], 'data_inicial': data_inicial, 'data_final': data_final,
    })
