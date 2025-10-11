"""
Views de Registro de Usuários
Sistema XBPneus
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backend.transportador.models import UsuarioTransportador
from backend.motorista.models import UsuarioMotorista
from backend.borracharia.models import UsuarioBorracharia
from backend.revenda.models import UsuarioRevenda
from backend.recapagem.models import UsuarioRecapagem


@api_view(['POST'])
@permission_classes([AllowAny])
def register_full_view(request):
    """
    Endpoint unificado para registro completo de usuários
    
    Suporta 5 tipos de usuários:
    - transportador
    - motorista
    - borracharia
    - revenda
    - recapagem
    """
    tipo_usuario = request.data.get('tipo_usuario')
    
    if not tipo_usuario:
        return Response({
            'error': 'Tipo de usuário é obrigatório',
            'tipos_validos': ['transportador', 'motorista', 'borracharia', 'revenda', 'recapagem']
        }, status=status.HTTP_400_BAD_REQUEST)
    
    tipo_usuario = tipo_usuario.lower()
    
    # Mapear tipo de usuário para modelo e serializer
    tipo_map = {
        'transportador': {
            'model': UsuarioTransportador,
            'required_fields': ['email', 'password', 'nome_razao_social', 'cnpj', 'telefone']
        },
        'motorista': {
            'model': UsuarioMotorista,
            'required_fields': ['email', 'password', 'nome_completo', 'cpf', 'cnh', 'categoria_cnh', 'telefone']
        },
        'borracharia': {
            'model': UsuarioBorracharia,
            'required_fields': ['email', 'password', 'nome_razao_social', 'cnpj', 'telefone']
        },
        'revenda': {
            'model': UsuarioRevenda,
            'required_fields': ['email', 'password', 'nome_razao_social', 'cnpj', 'telefone']
        },
        'recapagem': {
            'model': UsuarioRecapagem,
            'required_fields': ['email', 'password', 'nome_razao_social', 'cnpj', 'telefone']
        }
    }
    
    if tipo_usuario not in tipo_map:
        return Response({
            'error': f'Tipo de usuário inválido: {tipo_usuario}',
            'tipos_validos': list(tipo_map.keys())
        }, status=status.HTTP_400_BAD_REQUEST)
    
    config = tipo_map[tipo_usuario]
    model = config['model']
    required_fields = config['required_fields']
    
    # Validar campos obrigatórios
    missing_fields = []
    for field in required_fields:
        if field not in request.data or not request.data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return Response({
            'error': 'Campos obrigatórios faltando',
            'campos_faltando': missing_fields
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verificar se email já existe
    email = request.data.get('email')
    if model.objects.filter(email=email).exists():
        return Response({
            'error': 'Email já cadastrado'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verificar se CPF/CNPJ já existe (se aplicável)
    if 'cpf' in required_fields:
        cpf = request.data.get('cpf')
        if model.objects.filter(cpf=cpf).exists():
            return Response({
                'error': 'CPF já cadastrado'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    if 'cnpj' in required_fields:
        cnpj = request.data.get('cnpj')
        if model.objects.filter(cnpj=cnpj).exists():
            return Response({
                'error': 'CNPJ já cadastrado'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    if 'cnh' in required_fields:
        cnh = request.data.get('cnh')
        if model.objects.filter(cnh=cnh).exists():
            return Response({
                'error': 'CNH já cadastrada'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Criar usuário
        user_data = {}
        for field in required_fields:
            if field != 'password':
                user_data[field] = request.data[field]
        
        # Adicionar campos opcionais se presentes
        optional_fields = ['endereco', 'cidade', 'estado', 'cep']
        for field in optional_fields:
            if field in request.data:
                user_data[field] = request.data[field]
        
        # Criar usuário
        user = model.objects.create_user(
            **user_data,
            password=request.data['password']
        )
        
        return Response({
            'message': 'Cadastro realizado com sucesso! Aguarde aprovação do administrador.',
            'user': {
                'id': user.id,
                'email': user.email,
                'tipo_usuario': tipo_usuario,
                'aprovado': user.aprovado,
                'is_active': user.is_active
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Erro ao criar usuário: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

