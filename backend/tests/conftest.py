import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="tester@xbpneus.com",
        password="pass123",
        nome_razao_social="Tester User",
        cnpj="12345678000100",
        telefone="(11) 99999-9999",
        aprovado=True
    )

@pytest.fixture
def client_auth(user):
    client = APIClient()
    # obtain JWT
    from django.urls import reverse
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client

