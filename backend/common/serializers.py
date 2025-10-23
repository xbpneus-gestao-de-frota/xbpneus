from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Primeiro, valida as credenciais normalmente
        data = super().validate(attrs)
        
        # Verifica se o usuário está aprovado
        if hasattr(self.user, 'aprovado') and not self.user.aprovado:
            raise serializers.ValidationError(
                {'detail': 'Usuário não aprovado pelo administrador.'}
            )
        
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Adicionar user_role ao token
        # O modelo UsuarioTransportador é usado para todos os tipos de usuários
        # Por padrão, todos são transportadores
        if hasattr(user, 'motorista_externo_perfil'):
            token['user_role'] = 'motorista_externo'
        elif hasattr(user, 'usuariomotorista'):
            token['user_role'] = 'motorista'
        elif hasattr(user, 'usuarioborracharia'):
            token['user_role'] = 'borracharia'
        elif hasattr(user, 'usuariorevenda'):
            token['user_role'] = 'revenda'
        elif hasattr(user, 'usuariorecapagem'):
            token['user_role'] = 'recapagem'
        else:
            token['user_role'] = 'transportador'
        
        # Se for admin/superuser, sobrescrever
        if user.is_superuser or user.is_staff:
            token['user_role'] = 'admin'
        
        return token

