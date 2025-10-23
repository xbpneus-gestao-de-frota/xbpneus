from rest_framework_simplejwt.exceptions import InvalidToken

class CustomUserAuthenticationRule:
    """
    Regra de autenticação customizada para JWT que verifica se o usuário
    está ativo e aprovado.
    """
    def authenticate(self, user):
        # A autenticação básica do JWT já foi feita.
        # Aqui, verificamos as regras de negócio adicionais.
        
        if not user.is_active:
            # Esta verificação é redundante, pois o ModelBackend já a faz,
            # mas a mantemos para ser explícita no fluxo do SimpleJWT.
            raise InvalidToken("Usuário inativo.")
        
        # O campo 'aprovado' é customizado para o sistema XBPneus.
        # O problema no login da API é que a autenticação falha antes de chegar aqui,
        # mas esta regra é crucial para a validação do token após a obtenção.
        if hasattr(user, 'aprovado') and not user.aprovado:
            raise InvalidToken("Usuário não aprovado pelo administrador.")
            
        return user
