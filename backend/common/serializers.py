from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Adicionar user_role ao token
        # Assumindo que o usuário tem um campo 'tipo_cliente' que define o role
        if hasattr(user, 'tipo_cliente'):
            token['user_role'] = user.tipo_cliente
        else:
            # Fallback: verificar se é superuser/admin
            if user.is_superuser or user.is_staff:
                token['user_role'] = 'admin'
            else:
                token['user_role'] = 'transportador'  # Default
        
        return token

