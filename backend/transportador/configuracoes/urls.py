"""
URLs para o módulo de Configuracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfiguracaoSistemaViewSet, ParametroEmpresaViewSet, PerfilUsuarioViewSet, PermissaoCustomizadaViewSet

router = DefaultRouter()
router.register(r'configuracaosistemas', ConfiguracaoSistemaViewSet, basename='configuracaosistema')
router.register(r'parametroempresas', ParametroEmpresaViewSet, basename='parametroempresa')
router.register(r'perfilusuarios', PerfilUsuarioViewSet, basename='perfilusuario')
router.register(r'permissaocustomizadas', PermissaoCustomizadaViewSet, basename='permissaocustomizada')

urlpatterns = [
    path('', include(router.urls)),
]
