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
    
    # Estatísticas de frota
    total_veiculos = Vehicle.objects.count()
    veiculos_ativos = Vehicle.objects.filter(status='ATIVO').count()
    veiculos_manutencao = Vehicle.objects.filter(status='MANUTENCAO').count()
    
    # Estatísticas de pneus
    total_posicoes = Position.objects.count()
    posicoes_ocupadas = Position.objects.exclude(pneu_atual_codigo__isnull=True).exclude(pneu_atual_codigo='').count()
    
    # Estatísticas de manutenção
    os_abertas = OrdemServico.objects.filter(status='ABERTA').count()
    os_em_andamento = OrdemServico.objects.filter(status='EM_ANDAMENTO').count()
    os_atrasadas = OrdemServico.objects.filter(
        data_agendamento__lt=timezone.now(),
        status__in=['ABERTA', 'AGENDADA', 'EM_ANDAMENTO']
    ).count()
    
    # Estatísticas de estoque (últimos 30 dias)
    data_inicio = timezone.now() - timedelta(days=30)
    movimentacoes_periodo = MovimentacaoEstoque.objects.filter(
        data_movimentacao__gte=data_inicio
    )
    
    entradas = movimentacoes_periodo.filter(tipo='ENTRADA').count()
    saidas = movimentacoes_periodo.filter(tipo='SAIDA').count()
    
    # Veículos que precisam de manutenção
    veiculos_precisam_manutencao = []
    for veiculo in Vehicle.objects.filter(status='ATIVO'):
        if veiculo.precisa_manutencao():
            veiculos_precisam_manutencao.append({
                'placa': veiculo.placa,
                'modelo': veiculo.modelo,
                'km_atual': veiculo.km,
                'km_proxima_manutencao': veiculo.km_proxima_manutencao,
                'km_restante': veiculo.km_ate_manutencao()
            })
    
    # Últimas movimentações
    ultimas_movimentacoes = []
    for mov in MovimentacaoEstoque.objects.all().order_by('-data_movimentacao')[:5]:
        ultimas_movimentacoes.append({
            'tipo': mov.tipo,
            'data': mov.data_movimentacao.isoformat() if mov.data_movimentacao else None,
            'observacoes': mov.observacoes
        })
    
    # Últimas OS
    ultimas_os = []
    for os in OrdemServico.objects.all().order_by('-data_abertura')[:5]:
        ultimas_os.append({
            'numero': os.numero,
            'veiculo_placa': os.veiculo.placa if os.veiculo else None,
            'tipo': os.tipo,
            'status': os.status,
            'prioridade': os.prioridade,
            'data_abertura': os.data_abertura.isoformat() if os.data_abertura else None
        })
    
    dashboard_data = {
        'usuario': {
            'email': user.email,
            'nome': getattr(user, 'nome_razao_social', user.email),
            'tipo': 'transportador'
        },
        'frota': {
            'total_veiculos': total_veiculos,
            'veiculos_ativos': veiculos_ativos,
            'veiculos_manutencao': veiculos_manutencao,
            'veiculos_inativos': total_veiculos - veiculos_ativos - veiculos_manutencao,
            'precisam_manutencao': len(veiculos_precisam_manutencao),
            'veiculos_alerta': veiculos_precisam_manutencao[:3]  # Top 3
        },
        'pneus': {
            'total_posicoes': total_posicoes,
            'posicoes_ocupadas': posicoes_ocupadas,
            'posicoes_vazias': total_posicoes - posicoes_ocupadas,
            'taxa_ocupacao': round((posicoes_ocupadas / total_posicoes * 100), 1) if total_posicoes > 0 else 0
        },
        'manutencao': {
            'os_abertas': os_abertas,
            'os_em_andamento': os_em_andamento,
            'os_atrasadas': os_atrasadas,
            'total_pendentes': os_abertas + os_em_andamento,
            'ultimas_os': ultimas_os
        },
        'estoque': {
            'entradas_30d': entradas,
            'saidas_30d': saidas,
            'saldo_30d': entradas - saidas,
            'ultimas_movimentacoes': ultimas_movimentacoes
        },
        'alertas': {
            'veiculos_manutencao': veiculos_manutencao,
            'os_atrasadas': os_atrasadas,
            'veiculos_precisam_manutencao': len(veiculos_precisam_manutencao)
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

