from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalisePneusViewSet

router = DefaultRouter()
router.register(r'analise', AnalisePneusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

