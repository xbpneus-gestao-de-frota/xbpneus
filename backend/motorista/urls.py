from django.urls import path, include
from . import views
from . import motorista_externo_urls

urlpatterns = [
    path('register/', views.registro_motorista, name='motorista-register'),
    path('login/', views.login_motorista, name='motorista-login'),
    path('perfil/', views.perfil_motorista, name='motorista-perfil'),
    path('externo/', include(motorista_externo_urls)),
]