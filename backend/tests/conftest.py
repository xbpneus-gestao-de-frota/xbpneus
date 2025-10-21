import pytest
import django
from django.conf import settings
from django.contrib.auth import get_user_model

# Configurar as settings do Django para os testes
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_framework_simplejwt',
            'corsheaders',
            'drf_spectacular',
            'backend.transportador',
            'backend.motorista',
            'backend.borracharia',
            'backend.revenda',
            'backend.recapagem',
            'backend.common',
            'backend.core',
            'backend.jobs',
            # 'backend.usuarios', # Removido, pois AUTH_USER_MODEL aponta para transportador.UsuarioTransportador
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        SECRET_KEY='a-very-secret-key-for-testing',
        ROOT_URLCONF='config.urls', # Corrigido para config.urls
        USE_TZ=True,
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ],
        REST_FRAMEWORK={
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework_simplejwt.authentication.JWTAuthentication',
            ),
            'DEFAULT_PERMISSION_CLASSES': (
                'rest_framework.permissions.AllowAny', # Alterado para AllowAny para testar registro e login
            ),
            'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        },
        SPECTACULAR_SETTINGS={
            'TITLE': 'XBPneus API',
            'DESCRIPTION': 'Documentação da API do sistema XBPneus',
            'VERSION': '1.0.0',
            'SERVE_INCLUDE_SCHEMA': False,
        },
        AUTH_USER_MODEL='transportador.UsuarioTransportador',
    )
    django.setup()

from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="tester@xbpneus.com",
        password="pass123",
        nome_razao_social="Tester User",
        cnpj="12345678000100",
        telefone="(11) 99999-9999",
        is_active=True,
        aprovado=True
    )

@pytest.fixture
def client_auth(user):
    client = APIClient()
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client

