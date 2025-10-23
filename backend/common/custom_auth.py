from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model

class CustomUserAuthenticationRule:
    """
    Regra de autenticação customizada para JWT que verifica se o usuário
    está ativo e aprovado.
    """
    def authenticate(self, user):
        # A autenticação básica do JWT já foi feita.
        # Aqui, verificamos as regras de negócio adicionais.
        
        if not user.is_active:
            raise InvalidToken("Usuário inativo.")
        
        # O campo 'aprovado' é customizado para o sistema XBPneus.
        if hasattr(user, 'aprovado') and not user.aprovado:
            raise InvalidToken("Usuário não aprovado pelo administrador.")
            
        return user
