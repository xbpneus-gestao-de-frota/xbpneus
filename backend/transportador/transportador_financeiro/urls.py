from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DespesaViewSet, LancamentoViewSet

router = DefaultRouter()
router.register(r'despesas', DespesaViewSet)
router.register(r'lancamentos', LancamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

