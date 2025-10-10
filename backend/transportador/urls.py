from django.urls import path
from . import views
from .dashboard_views import dashboard_view, profile_view, me_view

urlpatterns = [
    path('register/', views.registro_transportador, name='transportador-register'),
    path('login/', views.login_transportador, name='transportador-login'),
    path('perfil/', views.perfil_transportador, name='transportador-perfil'),
    
    # Novos endpoints
    path('dashboard/', dashboard_view, name='transportador-dashboard'),
    path('profile/', profile_view, name='transportador-profile'),
    path('me/', me_view, name='transportador-me'),
]

