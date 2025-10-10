"""
Views para o módulo de Configuracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import ConfiguracaoSistema, ParametroEmpresa, PerfilUsuario, PermissaoCustomizada
from .serializers import ConfiguracaoSistemaSerializer, ParametroEmpresaSerializer, PerfilUsuarioSerializer, PermissaoCustomizadaSerializer


class ConfiguracaoSistemaViewSet(viewsets.ModelViewSet):
    """ViewSet para ConfiguracaoSistema"""
    permission_classes = [IsAuthenticated]
    serializer_class = ConfiguracaoSistemaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ConfiguracaoSistema.objects.all()
        return ConfiguracaoSistema.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class ParametroEmpresaViewSet(viewsets.ModelViewSet):
    """ViewSet para ParametroEmpresa"""
    permission_classes = [IsAuthenticated]
    serializer_class = ParametroEmpresaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ParametroEmpresa.objects.all()
        return ParametroEmpresa.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para PerfilUsuario"""
    permission_classes = [IsAuthenticated]
    serializer_class = PerfilUsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PerfilUsuario.objects.all()
        return PerfilUsuario.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class PermissaoCustomizadaViewSet(viewsets.ModelViewSet):
    """ViewSet para PermissaoCustomizada"""
    permission_classes = [IsAuthenticated]
    serializer_class = PermissaoCustomizadaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PermissaoCustomizada.objects.all()
        return PermissaoCustomizada.objects.filter(empresa=user.empresa)
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


