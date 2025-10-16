from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RelatorioTransportadorViewSet

router = DefaultRouter()
router.register(r'relatorios', RelatorioTransportadorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

