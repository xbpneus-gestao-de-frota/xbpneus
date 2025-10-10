from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registro_motorista, name='motorista-register'),
    path('login/', views.login_motorista, name='motorista-login'),
    path('perfil/', views.perfil_motorista, name='motorista-perfil'),
]
