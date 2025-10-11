"""
Views de Dashboard e Perfil para Transportador
Sistema XBPneus
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta

from backend.transportador.models import UsuarioTransportador
from backend.transportador.frota.models import Vehicle, Position
from backend.transportador.estoque.models import MovimentacaoEstoque
from backend.transportador.manutencao.models import OrdemServico


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    """
    Endpoint de dashboard com estatísticas gerais do transportador
    """
    user = request.user
    
    # Dados mockados para o dashboard do transportador
    dashboard_data = {
        'usuario': {
            'email': user.email,
            'nome': getattr(user, 'nome_razao_social', user.email),
            'tipo': 'transportador'
        },
        'frota': {
            'total_veiculos': 15,
            'veiculos_ativos': 12,
            'veiculos_manutencao': 2,
            'veiculos_inativos': 1,
            'precisam_manutencao': 3,
            'veiculos_alerta': [
                {'placa': 'ABC-1234', 'modelo': 'Caminhão A', 'km_restante': 500},
                {'placa': 'DEF-5678', 'modelo': 'Caminhão B', 'km_restante': 800}
            ]
        },
        'pneus': {
            'total_posicoes': 120,
            'posicoes_ocupadas': 100,
            'posicoes_vazias': 20,
            'taxa_ocupacao': 83.3
        },
        'manutencao': {
            'os_abertas': 5,
            'os_em_andamento': 3,
            'os_atrasadas': 1,
            'total_pendentes': 8,
            'ultimas_os': [
                {'numero': 'OS001', 'veiculo_placa': 'ABC-1234', 'tipo': 'Preventiva', 'status': 'ABERTA', 'prioridade': 'ALTA', 'data_abertura': '2025-10-10T10:00:00Z'},
                {'numero': 'OS002', 'veiculo_placa': 'DEF-5678', 'tipo': 'Corretiva', 'status': 'EM_ANDAMENTO', 'prioridade': 'MEDIA', 'data_abertura': '2025-10-09T14:30:00Z'}
            ]
        },
        'estoque': {
            'entradas_30d': 50,
            'saidas_30d': 30,
            'saldo_30d': 20,
            'ultimas_movimentacoes': [
                {'tipo': 'ENTRADA', 'data': '2025-10-10T11:00:00Z', 'observacoes': 'Recebimento de pneus novos'},
                {'tipo': 'SAIDA', 'data': '2025-10-09T16:00:00Z', 'observacoes': 'Envio para manutenção'}
            ]
        },
        'alertas': {
            'veiculos_manutencao': 2,
            'os_atrasadas': 1,
            'veiculos_precisam_manutencao': 3
        }
    }
    
    return Response(dashboard_data)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Endpoint de perfil do usuário transportador
    GET: Retorna dados do perfil
    PUT/PATCH: Atualiza dados do perfil
    """
    user = request.user
    
    if request.method == 'GET':
        # Retornar dados do perfil
        profile_data = {
            'id': user.id,
            'email': user.email,
            'nome_razao_social': getattr(user, 'nome_razao_social', ''),
            'cnpj': getattr(user, 'cnpj', ''),
            'telefone': getattr(user, 'telefone', ''),
            'aprovado': getattr(user, 'aprovado', False),
            'is_active': user.is_active,
            'criado_em': getattr(user, 'criado_em', None),
            'aprovado_em': getattr(user, 'aprovado_em', None),
            'aprovado_por': getattr(user, 'aprovado_por', None),
            'tipo_usuario': 'transportador',
            'empresa_id': getattr(user, 'empresa_id', None)
        }
        
        # Converter datas para string
        if profile_data['criado_em']:
            profile_data['criado_em'] = profile_data['criado_em'].isoformat()
        if profile_data['aprovado_em']:
            profile_data['aprovado_em'] = profile_data['aprovado_em'].isoformat()
        
        return Response(profile_data)
    
    elif request.method in ['PUT', 'PATCH']:
        # Atualizar dados do perfil
        campos_permitidos = ['nome_razao_social', 'telefone']
        
        for campo in campos_permitidos:
            if campo in request.data:
                setattr(user, campo, request.data[campo])
        
        user.save()
        
        return Response({
            'message': 'Perfil atualizado com sucesso',
            'email': user.email,
            'nome_razao_social': getattr(user, 'nome_razao_social', '')
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Endpoint simplificado para retornar dados básicos do usuário logado
    """
    user = request.user
    
    user_data = {
        'id': user.id,
        'email': user.email,
        'nome': getattr(user, 'nome_razao_social', user.email),
        'tipo': 'transportador',
        'aprovado': getattr(user, 'aprovado', False),
        'is_active': user.is_active,
        'is_superuser': user.is_superuser
    }
    
    return Response(user_data)

