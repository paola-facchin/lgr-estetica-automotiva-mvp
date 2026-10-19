from datetime import date
from decimal import Decimal
from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse
from .forms import PlacaForm, VeiculoForm
from .models import Cliente, Veiculo, Servico, MovimentacaoFinanceira

class PlacaTests(TestCase):
    def test_placa_antiga_e_mercosul(self):
        self.assertTrue(PlacaForm({'placa': 'abc-1234'}).is_valid())
        self.assertTrue(PlacaForm({'placa': 'abc1d23'}).is_valid())
        self.assertFalse(PlacaForm({'placa': '123'}).is_valid())

    def test_impede_placa_duplicada(self):
        cliente = Cliente.objects.create(nome='Cliente de teste', telefone='11999999999')
        Veiculo.objects.create(cliente=cliente, placa='ABC1D23', marca='Fiat', modelo='Argo')
        form = VeiculoForm({'cliente': cliente.id, 'placa': 'abc-1d23', 'marca': 'Fiat', 'modelo': 'Argo'})
        self.assertFalse(form.is_valid())
        self.assertIn('placa', form.errors)

class IntegracaoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='colaborador', password='SenhaForteTeste123!')
        self.client.force_login(self.user)
        c = Cliente.objects.create(nome='Cliente fictício', telefone='11999999999')
        self.v = Veiculo.objects.create(cliente=c, placa='ABC1D23', marca='Fiat', modelo='Argo')
        outro = Veiculo.objects.create(cliente=c, placa='DEF1234', marca='VW', modelo='Gol')
        Servico.objects.create(veiculo=self.v, descricao='Limpeza interna', data_servico=date(2026,10,15), valor=Decimal('180.00'))
        Servico.objects.create(veiculo=outro, descricao='Outro serviço', data_servico=date(2026,10,1), valor=Decimal('50.00'))

    def test_consulta_requer_login(self):
        self.client.logout()
        r = self.client.get(reverse('consulta'))
        self.assertEqual(r.status_code, 302)

    def test_consulta_por_placa_e_isolamento(self):
        r = self.client.get(reverse('consulta'), {'placa': 'abc-1d23'})
        self.assertRedirects(r, reverse('historico', kwargs={'placa':'ABC1D23'}))
        r = self.client.get(reverse('historico', kwargs={'placa':'ABC1D23'}))
        self.assertContains(r, 'Limpeza interna')
        self.assertNotContains(r, 'Outro serviço')

    def test_placa_inexistente(self):
        r = self.client.get(reverse('historico', kwargs={'placa':'ZZZ9Z99'}))
        self.assertContains(r, 'Veículo não encontrado')

    def test_colaborador_sem_permissao_nao_acessa_financeiro(self):
        r = self.client.get(reverse('financeiro_resumo'))
        self.assertEqual(r.status_code, 403)
        r = self.client.get(reverse('financeiro_novo'))
        self.assertEqual(r.status_code, 403)

    def test_resumo_financeiro_com_permissao(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_movimentacaofinanceira'))
        MovimentacaoFinanceira.objects.create(tipo='receita', descricao='Teste', valor=Decimal('180.00'), data_movimentacao=date(2026,10,15))
        MovimentacaoFinanceira.objects.create(tipo='despesa', descricao='Teste 2', valor=Decimal('30.00'), data_movimentacao=date(2026,10,15))
        r = self.client.get(reverse('financeiro_resumo'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['saldo'], Decimal('150.00'))

    def test_post_sem_csrf_quando_verificacao_ativada(self):
        from django.test import Client
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.user)
        response = cliente.post(reverse('cliente_novo'), {'nome': 'Incompleto', 'telefone':'111'})
        self.assertEqual(response.status_code, 403)
