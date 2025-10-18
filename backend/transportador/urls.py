from django.urls import path, include
from . import views
from .dashboard_views import dashboard_view, profile_view, me_view

urlpatterns = [
    path('register/', views.registro_transportador, name='transportador-register'),
    path('login/', views.login_transportador, name='transportador-login'),
    path('logout/', views.logout_transportador, name='transportador-logout'),
    path('perfil/', views.perfil_transportador, name='transportador-perfil'),
    
    # Novos endpoints
    path('dashboard/', dashboard_view, name='transportador-dashboard'),
    path('profile/', profile_view, name='transportador-profile'),
    path("me/", me_view, name="transportador-me"),
    path("motorista-externo/", include("backend.transportador.motorista_externo.urls")),
    path("pneus/", include("backend.transportador.pneus.urls")),
    path("frota/", include("backend.transportador.frota.urls")),
]

