"""Cria o primeiro administrador de maneira idempotente no deploy gratuito.

Variáveis DJANGO_SUPERUSER_USERNAME/PASSWORD são secretas e configuradas no Render,
não gravadas em código ou impressas em logs. Não altera senhas já existentes.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lgr.settings")

import django
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
if not username or not password:
    sys.exit("Configure DJANGO_SUPERUSER_USERNAME e DJANGO_SUPERUSER_PASSWORD no Render.")

User = get_user_model()
if User.objects.filter(username=username).exists():
    print("Administrador inicial já existe; credenciais anteriores preservadas.")
else:
    try:
        validate_password(password)
    except ValidationError:
        sys.exit("Senha do administrador não atende à política de segurança do Django.")
    User.objects.create_superuser(username=username, password=password)
    print("Administrador inicial criado, sem expor credenciais.")
