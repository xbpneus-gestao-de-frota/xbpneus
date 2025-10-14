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
                'usuariorecapagem',
                'motorista_externo_perfil'
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

