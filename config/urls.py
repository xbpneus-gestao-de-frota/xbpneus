from django.contrib import admin
from config import temp_user_creation_views, temp_migrate_views
from django.http import JsonResponse, HttpResponse
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from importlib import import_module

urlpatterns = [
    path("api/create-superuser-temp/", temp_user_creation_views.create_superuser_temp, name="create-superuser-temp"),
    path("api/create-test-users-temp/", temp_user_creation_views.create_test_users_temp, name="create-test-users-temp"),
    path("api/run-migrations-temp/", temp_migrate_views.run_migrations, name="run-migrations-temp"),
    path("api/show-migrations-temp/", temp_migrate_views.show_migrations, name="show-migrations-temp"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("admin/", admin.site.urls),
    
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

def try_include(prefix: str, module_path: str):
    try:
        mod = import_module(module_path)
        urlpatterns.append(path(prefix, include(mod)))
    except Exception as e:
        import logging
        logging.warning(f"Failed to include {module_path}: {e}")

# Módulos principais
try_include("api/transportador/", "backend.transportador.urls")
try_include("api/motorista/", "backend.motorista.urls")
try_include("api/borracharia/", "backend.borracharia.urls")
try_include("api/revenda/", "backend.revenda.urls")
try_include("api/recapagem/", "backend.recapagem.urls")

# Módulos do Transportador
try_include("api/transportador/frota/", "backend.transportador.frota.urls")
try_include("api/transportador/pneus/", "backend.transportador.pneus.urls")
try_include("api/transportador/manutencao/", "backend.transportador.manutencao.urls")
try_include("api/transportador/estoque/", "backend.transportador.estoque.urls")
try_include("api/transportador/loja/", "backend.transportador.loja.urls")
try_include("api/transportador/motorista-interno/", "backend.transportador.motorista_interno.urls")
try_include("api/transportador/custos/", "backend.transportador.custos.urls")
try_include("api/transportador/combustivel/", "backend.transportador.combustivel.urls")
try_include("api/transportador/multas/", "backend.transportador.multas.urls")
try_include("api/transportador/documentos/", "backend.transportador.documentos.urls")
try_include("api/transportador/viagens/", "backend.transportador.viagens.urls")
try_include("api/transportador/clientes/", "backend.transportador.clientes.urls")
try_include("api/transportador/fornecedores/", "backend.transportador.fornecedores.urls")
try_include("api/transportador/seguros/", "backend.transportador.seguros.urls")
try_include("api/transportador/contratos/", "backend.transportador.contratos.urls")
try_include("api/transportador/faturamento/", "backend.transportador.faturamento.urls")
try_include("api/transportador/pagamentos/", "backend.transportador.pagamentos.urls")
try_include("api/transportador/telemetria/", "backend.transportador.telemetria.urls")
try_include("api/transportador/rastreamento/", "backend.transportador.rastreamento.urls")
try_include("api/transportador/rotas/", "backend.transportador.rotas.urls")
try_include("api/transportador/entregas/", "backend.transportador.entregas.urls")
try_include("api/transportador/dashboards/", "backend.transportador.dashboards.urls")
try_include("api/transportador/notificacoes/", "backend.transportador.notificacoes.urls")
try_include("api/transportador/almoxarifado/", "backend.transportador.almoxarifado.urls")
try_include("api/transportador/relatorios/", "backend.transportador.relatorios.urls")
try_include("api/transportador/cargas/", "backend.transportador.cargas.urls")
try_include("api/transportador/pecas/", "backend.transportador.pecas.urls")
try_include("api/transportador/ferramentas/", "backend.transportador.ferramentas.urls")
try_include("api/transportador/epis/", "backend.transportador.epis.urls")
try_include("api/transportador/treinamentos/", "backend.transportador.treinamentos.urls")
try_include("api/transportador/compliance/", "backend.transportador.compliance.urls")
try_include("api/transportador/alertas/", "backend.transportador.alertas.urls")
try_include("api/transportador/integracoes/", "backend.transportador.integracoes.urls")
try_include("api/transportador/configuracoes/", "backend.transportador.configuracoes.urls")

# IA - Novo Módulo
try_include("api/transportador/ia/", "backend.transportador.ia_pneus.urls")

# Outros
try_include("api/reports/", "backend.reports.urls")
try_include("api/jobs/", "backend.jobs.urls")

# Healthcheck
def healthz(request):
    return JsonResponse({"status": "ok"})

# Metrics
def metrics(request):
    return HttpResponse("# Metrics", content_type="text/plain")

urlpatterns += [
    path("healthz/", healthz),
    path("metrics/", metrics),
]

