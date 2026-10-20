"""Verificações de navegação e recursos acessíveis da interface renovada."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class InterfaceTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="teste_interface", password="SenhaDeTeste123!")
        self.client.force_login(self.usuario)

    def test_painel_tem_navegacao_e_pular_para_conteudo(self):
        resposta = self.client.get(reverse("inicio"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'lang="pt-BR"')
        self.assertContains(resposta, 'href="#conteudo"')
        self.assertContains(resposta, 'aria-label="Menu principal"')
        self.assertContains(resposta, 'aria-current="page"')
        self.assertContains(resposta, "Bem-vindo à gestão da LGR")
        self.assertContains(resposta, "Consultar histórico por placa")

    def test_consulta_exibe_ajuda_associada_ao_input(self):
        resposta = self.client.get(reverse("consulta"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'aria-describedby="placa-ajuda"')
        self.assertContains(resposta, 'id="placa-ajuda"')
        self.assertContains(resposta, "Pesquisar histórico")
        self.assertContains(resposta, "Como funciona?")

    def test_consulta_invalida_com_alerta_textual(self):
        resposta = self.client.get(reverse("consulta"), {"placa": "ABC@1234"})
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'role="alert"')
        self.assertContains(resposta, "Informe uma placa válida")
