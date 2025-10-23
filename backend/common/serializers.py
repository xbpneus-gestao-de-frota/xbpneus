from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o campo 'username' e adiciona 'email'
        self.fields.pop(self.username_field, None)
        self.fields['email'] = serializers.CharField(write_only=True)
        self.fields['password'] = serializers.CharField(write_only=True)
        
    def validate(self, attrs):
        # O TokenObtainPairSerializer espera 'username' no attrs para a validação padrão.
        # Precisamos mapear 'email' para 'username' antes de chamar super().validate.
        attrs[self.username_field] = attrs['email']
        
        # Chama a validação padrão (autentica o usuário e verifica is_active)
        data = super().validate(attrs)

        # Autenticação bem-sucedida, agora verifica o campo 'aprovado'
        user = self.user
        
        if hasattr(user, 'aprovado') and not user.aprovado:
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

