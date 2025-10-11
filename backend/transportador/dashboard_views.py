"""
Views de Dashboard e Perfil para Transportador
Sistema XBPneus
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Avg, Q, F
from django.db import models
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
    Agora com dados REAIS do banco de dados
    """
    user = request.user
    
    # Obter a empresa do usuário
    empresa = getattr(user, 'empresa', None)
    
    # Se não houver empresa associada, retornar dados básicos
    if not empresa:
        dashboard_data = {
            'usuario': {
                'email': user.email,
                'nome': getattr(user, 'nome_razao_social', user.email),
                'tipo': 'transportador'
            },
            'frota': {
                'total_veiculos': 0,
                'veiculos_ativos': 0,
                'veiculos_manutencao': 0,
                'veiculos_inativos': 0,
                'precisam_manutencao': 0,
                'veiculos_alerta': []
            },
            'pneus': {
                'total_posicoes': 0,
                'posicoes_ocupadas': 0,
                'posicoes_vazias': 0,
                'taxa_ocupacao': 0
            },
            'manutencao': {
                'os_abertas': 0,
                'os_em_andamento': 0,
                'os_atrasadas': 0,
                'total_pendentes': 0,
                'ultimas_os': []
            },
            'estoque': {
                'entradas_30d': 0,
                'saidas_30d': 0,
                'saldo_30d': 0,
                'ultimas_movimentacoes': []
            },
            'alertas': {
                'veiculos_manutencao': 0,
                'os_atrasadas': 0,
                'veiculos_precisam_manutencao': 0
            },
            'mensagem': 'Nenhuma empresa associada ao usuário. Entre em contato com o administrador.'
        }
        return Response(dashboard_data)
    
    # Consultar dados REAIS do banco de dados
    
    # FROTA
    veiculos = Vehicle.objects.filter(empresa=empresa)
    total_veiculos = veiculos.count()
    veiculos_ativos = veiculos.filter(status='ATIVO').count()
    veiculos_manutencao = veiculos.filter(status='MANUTENCAO').count()
    veiculos_inativos = veiculos.filter(status='INATIVO').count()
    
    # Veículos que precisam de manutenção (exemplo: km_atual > km_proxima_manutencao)
    veiculos_precisam_manutencao = veiculos.filter(
        Q(km_proxima_manutencao__isnull=False) & 
        Q(km_atual__gte=F('km_proxima_manutencao'))
    ).count()
    
    # Alertas de veículos próximos da manutenção (500km antes)
    veiculos_alerta_qs = veiculos.filter(
        Q(km_proxima_manutencao__isnull=False) &
        Q(km_atual__gte=F('km_proxima_manutencao') - 500) &
        Q(km_atual__lt=F('km_proxima_manutencao'))
    )[:5]
    
    veiculos_alerta = []
    for v in veiculos_alerta_qs:
        km_restante = v.km_proxima_manutencao - v.km_atual if v.km_proxima_manutencao else 0
        veiculos_alerta.append({
            'placa': v.placa,
            'modelo': v.modelo,
            'km_restante': km_restante
        })
    
    # PNEUS (Posições)
    posicoes = Position.objects.filter(veiculo__empresa=empresa)
    total_posicoes = posicoes.count()
    posicoes_ocupadas = posicoes.filter(pneu__isnull=False).count()
    posicoes_vazias = total_posicoes - posicoes_ocupadas
    taxa_ocupacao = round((posicoes_ocupadas / total_posicoes * 100), 1) if total_posicoes > 0 else 0
    
    # MANUTENÇÃO
    ordens_servico = OrdemServico.objects.filter(veiculo__empresa=empresa)
    os_abertas = ordens_servico.filter(status='ABERTA').count()
    os_em_andamento = ordens_servico.filter(status='EM_ANDAMENTO').count()
    
    # OS atrasadas (data_prevista_conclusao < hoje e status != CONCLUIDA)
    hoje = timezone.now()
    os_atrasadas = ordens_servico.filter(
        data_prevista_conclusao__lt=hoje,
        status__in=['ABERTA', 'EM_ANDAMENTO']
    ).count()
    
    total_pendentes = os_abertas + os_em_andamento
    
    # Últimas OS
    ultimas_os_qs = ordens_servico.order_by('-data_abertura')[:5]
    ultimas_os = []
    for os in ultimas_os_qs:
        ultimas_os.append({
            'numero': os.numero_os,
            'veiculo_placa': os.veiculo.placa if os.veiculo else 'N/A',
            'tipo': os.tipo,
            'status': os.status,
            'prioridade': getattr(os, 'prioridade', 'MEDIA'),
            'data_abertura': os.data_abertura.isoformat() if os.data_abertura else None
        })
    
    # ESTOQUE
    data_30d_atras = hoje - timedelta(days=30)
    movimentacoes = MovimentacaoEstoque.objects.filter(
        empresa=empresa,
        data__gte=data_30d_atras
    )
    
    entradas_30d = movimentacoes.filter(tipo='ENTRADA').count()
    saidas_30d = movimentacoes.filter(tipo='SAIDA').count()
    saldo_30d = entradas_30d - saidas_30d
    
    # Últimas movimentações
    ultimas_movimentacoes_qs = MovimentacaoEstoque.objects.filter(
        empresa=empresa
    ).order_by('-data')[:5]
    
    ultimas_movimentacoes = []
    for mov in ultimas_movimentacoes_qs:
        ultimas_movimentacoes.append({
            'tipo': mov.tipo,
            'data': mov.data.isoformat() if mov.data else None,
            'observacoes': getattr(mov, 'observacoes', '')
        })
    
    # Montar resposta
    dashboard_data = {
        'usuario': {
            'email': user.email,
            'nome': getattr(user, 'nome_razao_social', user.email),
            'tipo': 'transportador',
            'empresa': empresa.nome if empresa else None
        },
        'frota': {
            'total_veiculos': total_veiculos,
            'veiculos_ativos': veiculos_ativos,
            'veiculos_manutencao': veiculos_manutencao,
            'veiculos_inativos': veiculos_inativos,
            'precisam_manutencao': veiculos_precisam_manutencao,
            'veiculos_alerta': veiculos_alerta
        },
        'pneus': {
            'total_posicoes': total_posicoes,
            'posicoes_ocupadas': posicoes_ocupadas,
            'posicoes_vazias': posicoes_vazias,
            'taxa_ocupacao': taxa_ocupacao
        },
        'manutencao': {
            'os_abertas': os_abertas,
            'os_em_andamento': os_em_andamento,
            'os_atrasadas': os_atrasadas,
            'total_pendentes': total_pendentes,
            'ultimas_os': ultimas_os
        },
        'estoque': {
            'entradas_30d': entradas_30d,
            'saidas_30d': saidas_30d,
            'saldo_30d': saldo_30d,
            'ultimas_movimentacoes': ultimas_movimentacoes
        },
        'alertas': {
            'veiculos_manutencao': veiculos_manutencao,
            'os_atrasadas': os_atrasadas,
            'veiculos_precisam_manutencao': veiculos_precisam_manutencao
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

