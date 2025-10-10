from rest_framework import viewsets, permissions
from .models import Empresa
from .serializers import EmpresaSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all().order_by("id")
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated]



from rest_framework.decorators import api_view, permission_classes as drf_permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import Transportador

@api_view(['POST'])
@drf_permission_classes([AllowAny])
def register_transportador(request):
    """
    Endpoint para cadastro de transportador.
    Cria registro com status PENDENTE aguardando aprovação do admin.
    """
    data = request.data
    
    # Validar campos obrigatórios
    required_fields = ['nome', 'cnpj', 'email', 'senha', 'contato']
    for field in required_fields:
        if not data.get(field):
            return Response(
                {'detail': f'Campo obrigatório: {field}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Verificar se email já existe
    if Transportador.objects.filter(email=data['email']).exists():
        return Response(
            {'detail': 'Email já cadastrado'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verificar se CNPJ já existe
    if Transportador.objects.filter(cnpj=data['cnpj']).exists():
        return Response(
            {'detail': 'CNPJ já cadastrado'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Criar registro de transportador com status PENDENTE
    try:
        transportador = Transportador.objects.create(
            razao=data['nome'],
            cnpj=data['cnpj'],
            email=data['email'],
            senha=make_password(data['senha']),
            telefone=data.get('contato', ''),
            estado=data.get('estado', ''),
            cidade=data.get('cidade', ''),
            status='PENDENTE'
        )
        
        return Response({
            'detail': 'Cadastro realizado com sucesso! Aguarde aprovação do administrador.',
            'transportador': {
                'id': transportador.id,
                'nome': transportador.razao,
                'email': transportador.email,
                'status': transportador.status
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'detail': f'Erro ao criar cadastro: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

