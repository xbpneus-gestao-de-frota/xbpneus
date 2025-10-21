import base64
import binascii
import os
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Avg, Count, Max
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .core.visao_computacional import VisaoComputacionalAvancada
from .models import AnaliseIA, Gamificacao, Garantia
from .permissions import IsTransportadorOrAdmin
from .serializers import AnaliseIASerializer, GamificacaoSerializer, GarantiaSerializer


class AnaliseIAViewSet(viewsets.ModelViewSet):
    """
    ViewSet para análises de IA
    Acesso: Usuários Transportador e Admins
    """
    queryset = AnaliseIA.objects.all()
    serializer_class = AnaliseIASerializer
    permission_classes = [IsAuthenticated, IsTransportadorOrAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        """Retorna apenas análises do usuário logado (ou todas se admin)"""
        if self.request.user.is_staff:
            return AnaliseIA.objects.all()
        return AnaliseIA.objects.filter(usuario=self.request.user)

    @action(detail=False, methods=['post'])
    def analisar(self, request):
        """
        Endpoint para realizar análise de imagem/vídeo/áudio
        """
        payload = request.data
        tipo_analise = payload.get('tipo_analise', 'imagem')
        tipo_validos = {choice[0] for choice in AnaliseIA._meta.get_field('tipo_analise').choices}

        if tipo_analise not in tipo_validos:
            return Response(
                {'detail': f"Tipo de análise inválido. Valores aceitos: {', '.join(sorted(tipo_validos))}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        arquivo = self._extrair_arquivo(payload)
        if not arquivo:
            return Response(
                {'detail': 'É necessário enviar um arquivo ou arquivo_base64 para análise.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        modo_analise = payload.get('modo_analise') or payload.get('categoria') or 'geral'
        analisador = VisaoComputacionalAvancada()

        resultado_analise: Dict[str, Any]
        tempo_processamento = 0.0
        temp_path: Optional[str] = None
        try:
            temp_path = self._salvar_temporario(arquivo)
            inicio = time.perf_counter()
            resultado_analise = analisador.analisar_imagem(temp_path, modo_analise)
            tempo_processamento = time.perf_counter() - inicio
        except Exception as exc:  # pragma: no cover - proteção extra
            return Response(
                {'detail': f'Não foi possível processar a análise: {exc}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

        precisao = self._obter_precisao(resultado_analise)
        status_final = 'concluida' if not resultado_analise.get('erro') else 'erro'

        arquivo.seek(0)
        arquivo_final = ContentFile(arquivo.read(), name=arquivo.name)

        with transaction.atomic():
            analise = AnaliseIA.objects.create(
                usuario=request.user,
                tipo_analise=tipo_analise,
                arquivo=arquivo_final,
                resultado=resultado_analise,
                precisao=precisao,
                tempo_processamento=tempo_processamento,
                status=status_final,
            )

        serializer = self.get_serializer(analise)
        resposta = {
            'message': 'Análise concluída com sucesso' if status_final == 'concluida' else 'Análise registrada com erros',
            'analise': serializer.data,
            'resumo': {
                'precisao': precisao,
                'tempo_processamento': tempo_processamento,
                'modo_analise': modo_analise,
                'confianca': resultado_analise.get('confianca'),
            },
        }

        return Response(resposta, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Retorna métricas e estatísticas do dashboard
        """
        analises = self.get_queryset()

        if not analises.exists():
            return Response({
                'total_analises': 0,
                'precisao_media': 0.0,
                'tempo_medio': 0.0,
                'por_tipo': [],
                'status_resumo': [],
                'serie_temporal': [],
                'ultima_analise': None,
            })

        agregados = analises.aggregate(
            total=Count('id'),
            precisao_media=Avg('precisao'),
            tempo_medio=Avg('tempo_processamento'),
        )

        por_tipo = [
            {
                'tipo_analise': item['tipo_analise'],
                'total': item['total'],
                'precisao_media': float(item['precisao_media'] or 0.0),
                'ultima_analise': item['ultima_analise'].isoformat() if item['ultima_analise'] else None,
            }
            for item in analises
            .values('tipo_analise')
            .annotate(total=Count('id'), precisao_media=Avg('precisao'), ultima_analise=Max('data_analise'))
            .order_by('tipo_analise')
        ]

        status_resumo = [
            {
                'status': item['status'],
                'total': item['total'],
            }
            for item in analises.values('status').annotate(total=Count('id')).order_by('status')
        ]

        serie_temporal = [
            {
                'dia': item['dia'].isoformat(),
                'total': item['total'],
                'precisao_media': float(item['precisao_media'] or 0.0),
            }
            for item in analises
            .annotate(dia=TruncDate('data_analise'))
            .values('dia')
            .annotate(total=Count('id'), precisao_media=Avg('precisao'))
            .order_by('dia')
        ]

        ultima = analises.order_by('-data_analise').first()
        ultima_serializada = self.get_serializer(ultima).data if ultima else None

        return Response({
            'total_analises': agregados['total'],
            'precisao_media': float(agregados['precisao_media'] or 0.0),
            'tempo_medio': float(agregados['tempo_medio'] or 0.0),
            'por_tipo': por_tipo,
            'status_resumo': status_resumo,
            'serie_temporal': serie_temporal,
            'ultima_analise': ultima_serializada,
            'atualizado_em': timezone.now().isoformat(),
        })

    # Métodos utilitários -----------------------------------------------------------------

    def _extrair_arquivo(self, payload) -> Optional[ContentFile]:
        """Extrai arquivo do payload, aceitando upload direto ou base64."""
        arquivo = payload.get('arquivo')
        if arquivo:
            return arquivo

        arquivo_base64 = payload.get('arquivo_base64')
        if not arquivo_base64:
            return None

        nome = payload.get('nome_arquivo') or f'analise_{uuid4().hex}.jpg'
        try:
            conteudo = base64.b64decode(arquivo_base64)
        except (binascii.Error, TypeError, ValueError):
            return None

        return ContentFile(conteudo, name=nome)

    def _salvar_temporario(self, arquivo: ContentFile) -> str:
        """Grava arquivo em um arquivo temporário para ser processado."""
        arquivo.seek(0)
        sufixo = Path(arquivo.name or 'analise').suffix or '.tmp'
        with tempfile.NamedTemporaryFile(delete=False, suffix=sufixo) as tmp:
            tmp.write(arquivo.read())
            return tmp.name

    @staticmethod
    def _obter_precisao(resultado: Dict[str, Any]) -> float:
        """Normaliza o valor de precisão/confianca retornado pelos módulos de IA."""
        candidatos = [
            resultado.get('precisao'),
            resultado.get('confianca'),
            resultado.get('confidence'),
        ]
        for valor in candidatos:
            try:
                if valor is not None:
                    return float(valor)
            except (TypeError, ValueError):
                continue
        return 0.0


class GamificacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gamificação
    Acesso: Usuários Transportador e Admins
    """
    queryset = Gamificacao.objects.all()
    serializer_class = GamificacaoSerializer
    permission_classes = [IsAuthenticated, IsTransportadorOrAdmin]
    
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        """
        Retorna o ranking de usuários
        """
        ranking = Gamificacao.objects.all()[:10]
        serializer = self.get_serializer(ranking, many=True)
        return Response(serializer.data)


class GarantiaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para garantias
    Acesso: Usuários Transportador e Admins
    """
    queryset = Garantia.objects.all()
    serializer_class = GarantiaSerializer
    permission_classes = [IsAuthenticated, IsTransportadorOrAdmin]
    
    def get_queryset(self):
        """Retorna apenas garantias do usuário logado (ou todas se admin)"""
        if self.request.user.is_staff:
            return Garantia.objects.all()
        return Garantia.objects.filter(usuario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        """
        Aprova uma garantia (apenas admins)
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'Apenas administradores podem aprovar garantias'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        garantia = self.get_object()
        garantia.status = 'aprovada'
        garantia.save()
        
        return Response({
            'message': 'Garantia aprovada com sucesso',
            'protocolo': garantia.protocolo
        })

