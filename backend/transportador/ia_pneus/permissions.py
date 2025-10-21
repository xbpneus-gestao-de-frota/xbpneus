from django.contrib.auth import get_user_model
from rest_framework import permissions


def _is_transportador_user(user) -> bool:
    """Verifica se o usuário autenticado pertence ao módulo de transportador."""
    try:
        transportador_model = get_user_model()
    except Exception:  # pragma: no cover - fallback em caso de configuração incompleta
        transportador_model = None

    if transportador_model and isinstance(user, transportador_model):
        return True

    atributos_relacionados = ("transportador", "usuariotransportador", "usuario_transportador")
    return any(hasattr(user, attr) for attr in atributos_relacionados)


class IsTransportador(permissions.BasePermission):
    """
    Permissão que permite acesso apenas para usuários do tipo Transportador
    """
    
    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user or not request.user.is_authenticated:
            return False

        return _is_transportador_user(request.user)


class IsTransportadorOrAdmin(permissions.BasePermission):
    """
    Permissão que permite acesso para usuários Transportador ou Admin
    """
    
    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins têm acesso total
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Verifica se é um usuário transportador
        return _is_transportador_user(request.user)

