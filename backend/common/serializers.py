from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Primeiro, valida as credenciais normalmente
        data = super().validate(attrs)
        
        # Verifica se o usuário está aprovado (exceto superusuários)
        if not self.user.is_superuser:
            # Lista de tipos de usuários que possuem campo 'aprovado'
            user_types = [
                'usuariotransportador',
                'usuariomotorista', 
                'usuarioborracharia',
                'usuariorevenda',
                'usuariorecapagem'
            ]
            
            # Verifica cada tipo de usuário através do relacionamento reverso
            for user_type in user_types:
                if hasattr(self.user, user_type):
                    user_profile = getattr(self.user, user_type)
                    if hasattr(user_profile, 'aprovado') and not user_profile.aprovado:
                        raise serializers.ValidationError(
                            "Usuário aguardando aprovação do administrador. "
                            "Por favor, aguarde a aprovação para acessar o sistema."
                        )
                    break  # Encontrou o tipo de usuário, não precisa continuar
        
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

