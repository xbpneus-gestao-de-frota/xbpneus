from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet, register_transportador

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')

urlpatterns = [
    path('transportador/register/', register_transportador, name='transportador-register'),
    path('', include(router.urls)),
]
