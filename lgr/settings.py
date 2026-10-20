import os
import dj_database_url
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'development-only-change-before-deployment'
    else:
        raise ImproperlyConfigured('Defina DJANGO_SECRET_KEY no ambiente para producao.')

ALLOWED_HOSTS = [x.strip() for x in os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if x.strip()]
CSRF_TRUSTED_ORIGINS = [x.strip() for x in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if x.strip()]
# O Render informa automaticamente o hostname efetivo; não usamos curingas.
RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '').strip()
if RENDER_HOSTNAME:
    if RENDER_HOSTNAME not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_HOSTNAME)
    render_origin = f'https://{RENDER_HOSTNAME}'
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'core',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'lgr.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [], 'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'lgr.wsgi.application'

if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ['DATABASE_URL'],
            conn_max_age=60,
            conn_health_checks=True,
        )
    }
elif os.environ.get('POSTGRES_DB'):
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {'sslmode': os.environ.get('POSTGRES_SSLMODE', 'prefer')},
    }}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'
SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
# Evita loop de redirecionamento HTTPS ao executar atrás do proxy TLS do Render.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG and os.getenv('DJANGO_SSL_REDIRECT', 'true').lower() == 'true'
SECURE_HSTS_SECONDS = 31536000 if not DEBUG and os.getenv('DJANGO_ENABLE_HSTS', 'false').lower() == 'true' else 0
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
# Erros do Django aparecem no painel Logs do provedor, sem expor detalhes ao usuário.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {
        'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
    },
}
