import base64

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from backend.transportador.ia_pneus.models import AnaliseIA


@pytest.fixture(autouse=True)
def media_storage(settings, tmp_path):
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    settings.MEDIA_ROOT = str(media_dir)
    return media_dir


@pytest.mark.django_db
def test_analisar_cria_registro(client_auth):
    imagem = SimpleUploadedFile("pneu.jpg", b"fake-image-bytes", content_type="image/jpeg")

    response = client_auth.post(
        reverse("analise-analisar"),
        data={
            "tipo_analise": "imagem",
            "modo_analise": "geral",
            "arquivo": imagem,
        },
        format="multipart",
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["analise"]["status"] in {"concluida", "erro"}
    assert "resumo" in payload
    assert AnaliseIA.objects.count() == 1


@pytest.mark.django_db
def test_analisar_com_base64(client_auth):
    conteudo = base64.b64encode(b"imagem-ia-test").decode()

    response = client_auth.post(
        reverse("analise-analisar"),
        data={
            "tipo_analise": "imagem",
            "arquivo_base64": conteudo,
            "nome_arquivo": "pneu_base64.jpg",
        },
        format="json",
    )

    assert response.status_code == 201
    assert AnaliseIA.objects.count() == 1


@pytest.mark.django_db
def test_dashboard_retorna_metricas(client_auth, user):
    other_user = get_user_model().objects.create_user(
        email="outro@xbpneus.com",
        password="senha123",
        nome_razao_social="Outro Usuario",
        cnpj="09876543000100",
        telefone="(11) 98888-8888",
        is_active=True,
        aprovado=True,
    )

    AnaliseIA.objects.create(
        usuario=user,
        tipo_analise="imagem",
        arquivo=SimpleUploadedFile("pneu1.jpg", b"img1", content_type="image/jpeg"),
        resultado={"confianca": 0.8},
        precisao=0.8,
        tempo_processamento=1.2,
        status="concluida",
    )

    AnaliseIA.objects.create(
        usuario=user,
        tipo_analise="video",
        arquivo=SimpleUploadedFile("pneu2.mp4", b"img2", content_type="video/mp4"),
        resultado={"confianca": 0.6},
        precisao=0.6,
        tempo_processamento=2.4,
        status="concluida",
    )

    AnaliseIA.objects.create(
        usuario=other_user,
        tipo_analise="imagem",
        arquivo=SimpleUploadedFile("pneu3.jpg", b"img3", content_type="image/jpeg"),
        resultado={"confianca": 0.9},
        precisao=0.9,
        tempo_processamento=2.0,
        status="concluida",
    )

    response = client_auth.get(reverse("analise-dashboard"))
    assert response.status_code == 200

    dados = response.json()
    assert dados["total_analises"] == 2
    assert pytest.approx(dados["precisao_media"], rel=1e-3) == 0.7
    assert len(dados["por_tipo"]) == 2
    tipos = {item["tipo_analise"] for item in dados["por_tipo"]}
    assert tipos == {"imagem", "video"}
    assert dados["ultima_analise"] is not None
