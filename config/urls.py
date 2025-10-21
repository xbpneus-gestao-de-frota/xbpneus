from django.contrib import admin
from config import temp_user_creation_views, temp_migrate_views, temp_approval_views
from django.http import JsonResponse, HttpResponse
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from backend.common.views import CustomTokenObtainPairView
from backend.common.auth_views import logout_view, me_view
from backend.common.register_views import register_full_view
from backend.transportador.urls import TRANSPORTADOR_MODULES
from importlib import import_module

urlpatterns = [
    path("api/create-superuser-temp/", temp_user_creation_views.create_superuser_temp, name="create-superuser-temp"),
    path("api/create-test-users-temp/", temp_user_creation_views.create_test_users_temp, name="create-test-users-temp"),
    path("api/run-migrations-temp/", temp_migrate_views.run_migrations, name="run-migrations-temp"),
    path("api/show-migrations-temp/", temp_migrate_views.show_migrations, name="show-migrations-temp"),
    path("api/make-migrations-temp/", temp_migrate_views.make_migrations, name="make-migrations-temp"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("admin/", admin.site.urls),
    
    # Autenticação JWT
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    # Autenticação unificada (compatibilidade com frontend)
    path("api/auth/logout/", logout_view, name="auth-logout"),
    path("api/auth/me/", me_view, name="auth-me"),
    
    # Registro de usuários
    path("api/users/register_full/", register_full_view, name="users-register-full"),
    path("api/approve-motorista-externo/<int:user_id>/", temp_approval_views.approve_motorista_externo, name="approve-motorista-externo"),
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
for prefix, module_path in TRANSPORTADOR_MODULES.items():
    try_include(f"api/transportador/{prefix}/", module_path)

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

