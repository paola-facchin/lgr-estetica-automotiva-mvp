"""Testes do endpoint público de saúde para monitoramento externo."""
from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse


class HealthEndpointTests(TestCase):
    def test_responde_sem_login_e_com_banco_disponivel(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_retorna_503_quando_banco_falha(self):
        with patch("core.health.connection.cursor", side_effect=DatabaseError("indisponivel")):
            response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "indisponivel"})
        self.assertNotIn("DatabaseError", response.content.decode())

    def test_rejeita_metodos_que_alteram_servidor(self):
        response = self.client.post(reverse("health"), {})
        self.assertEqual(response.status_code, 405)
