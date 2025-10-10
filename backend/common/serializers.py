from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Adicionar user_role ao token
        # O modelo UsuarioTransportador é usado para todos os tipos de usuários
        # Por padrão, todos são transportadores
        token['user_role'] = 'transportador'
        
        # Se for admin/superuser, sobrescrever
        if user.is_superuser or user.is_staff:
            token['user_role'] = 'admin'
        
        return token

