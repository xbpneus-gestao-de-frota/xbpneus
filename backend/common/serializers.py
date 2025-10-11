from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Primeiro, valida as credenciais normalmente
        data = super().validate(attrs)
        
        # Verifica se o usuário está aprovado (exceto superusuários)
        if not self.user.is_superuser and not self.user.aprovado:
            raise serializers.ValidationError(
                "Usuário aguardando aprovação do administrador. "
                "Por favor, aguarde a aprovação para acessar o sistema."
            )
        
        return data
    
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

