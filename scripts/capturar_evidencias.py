"""Gera capturas REAIS do Django rodando no CI, com dados 100% fictícios."""
import os
import secrets
import subprocess
import sys
import time
import urllib.request
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lgr.settings")
import django

django.setup()

from django.contrib.auth.models import Permission, User
from core.models import Cliente, Servico, Veiculo
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765"
DEST = Path("docs/evidencias")
DEST.mkdir(parents=True, exist_ok=True)

# Um banco de testes isolado é criado pela execução no GitHub Actions.
# Não utilizar dados pessoais, senhas de produção ou serviços externos.
username = "usuario_demo"
password = secrets.token_urlsafe(24)
user = User.objects.create_user(username=username, password=password)
user.user_permissions.add(
    Permission.objects.get(codename="view_movimentacaofinanceira"),
    Permission.objects.get(codename="add_movimentacaofinanceira"),
)
cliente = Cliente.objects.create(nome="Cliente Fictício", telefone="00000000000")
veiculo = Veiculo.objects.create(
    cliente=cliente, placa="ABC1D23", marca="Fiat", modelo="Argo", cor="Prata"
)
for descricao, dia, valor in [
    ("Limpeza interna", date(2026, 10, 15), "180.00"),
    ("Polimento", date(2026, 9, 2), "450.00"),
    ("Higienização", date(2026, 8, 20), "250.00"),
]:
    Servico.objects.create(
        veiculo=veiculo,
        descricao=descricao,
        data_servico=dia,
        valor=Decimal(valor),
        observacoes="Registro fictício para demonstração.",
    )

server = subprocess.Popen(
    [sys.executable, "manage.py", "runserver", "127.0.0.1:8765", "--noreload"],
    env=os.environ.copy(),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT,
)

def aguardar_servidor():
    for _ in range(80):
        if server.poll() is not None:
            raise RuntimeError("O servidor Django foi encerrado inesperadamente.")
        try:
            urllib.request.urlopen(f"{URL}/contas/login/", timeout=1)
            return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError("O servidor Django não iniciou a tempo.")

def autenticar(pagina):
    pagina.goto(f"{URL}/contas/login/", wait_until="networkidle")
    pagina.get_by_label("Usuário").fill(username)
    pagina.get_by_label("Senha").fill(password)
    pagina.get_by_role("button", name="Entrar").click()
    pagina.get_by_role("heading", name="Bem-vindo à gestão da LGR").wait_for()

try:
    aguardar_servidor()
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True, args=["--no-sandbox"])
        desktop = navegador.new_context(viewport={"width": 1366, "height": 850}, device_scale_factor=1)
        pagina = desktop.new_page()
        autenticar(pagina)
        pagina.screenshot(path=str(DEST / "01-painel-inicial.png"), full_page=True)
        print("CAPTURA 1: painel inicial servido pelo Django, usuário fictício autenticado.", flush=True)

        pagina.get_by_role("link", name="Consultar histórico por placa").click()
        pagina.get_by_label("Placa do veículo").fill("ABC1D23")
        pagina.get_by_role("button", name="Pesquisar histórico").click()
        pagina.get_by_role("heading", name="Histórico do veículo").wait_for()
        assert pagina.get_by_text("Limpeza interna").is_visible()
        assert pagina.get_by_text("Polimento", exact=True).is_visible()
        assert pagina.get_by_text("Higienização", exact=True).is_visible()
        pagina.screenshot(path=str(DEST / "02-historico-servicos.png"), full_page=True)
        print("CAPTURA 2: histórico ABC1D23 consultado no banco de testes.", flush=True)

        celular = navegador.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=1,
            is_mobile=True,
            has_touch=True,
        )
        pagina_movel = celular.new_page()
        autenticar(pagina_movel)
        pagina_movel.goto(f"{URL}/consulta/", wait_until="networkidle")
        pagina_movel.get_by_label("Placa do veículo").fill("ABC@1234")
        pagina_movel.get_by_role("button", name="Pesquisar histórico").click()
        aviso = pagina_movel.get_by_role("alert")
        assert aviso.is_visible()
        assert "Informe uma placa válida" in aviso.inner_text()

        # Navegação por teclado, com o anel de foco visível e erro textual.
        campo = pagina_movel.get_by_label("Placa do veículo")
        for _ in range(30):
            pagina_movel.keyboard.press("Tab")
            if campo.evaluate("(el) => document.activeElement === el"):
                break
        assert campo.evaluate("(el) => document.activeElement === el"), "Campo não alcançado por teclado."
        foco = campo.evaluate(
            "(el) => ({ estilo: getComputedStyle(el).outlineStyle, "
            "largura: getComputedStyle(el).outlineWidth, "
            "cor: getComputedStyle(el).outlineColor })"
        )
        assert foco["estilo"] == "solid", f"Foco visual ausente: {foco}"
        assert float(foco["largura"].replace("px", "")) >= 3, foco
        pagina_movel.screenshot(path=str(DEST / "03-acessibilidade-foco-e-erro.png"), full_page=True)
        print(f"CAPTURA 3: foco visível por teclado + erro em texto, mobile 390px. {foco}", flush=True)
        print("CAPTURAS CONCLUÍDAS: 3 imagens reais geradas do sistema em execução.", flush=True)
        navegador.close()
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
