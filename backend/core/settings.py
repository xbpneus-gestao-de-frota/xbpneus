from .base_settings import *

# --- Configurações de Autenticação ---
SIMPLE_JWT = {
    'USER_AUTHENTICATION_RULE': 'backend.common.custom_auth.CustomUserAuthenticationRule',
}


AUTH_USER_MODEL = 'transportador.UsuarioTransportador'

AUTHENTICATION_BACKENDS = [
    'backend.common.backends.backends.CustomAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

