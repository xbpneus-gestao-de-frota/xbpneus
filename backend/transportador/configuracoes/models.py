from django.conf import settings
"""
Models para o módulo de Configuracoes
Sistema XBPneus - Gestão de Frotas de Transporte
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class ConfiguracaoSistema(models.Model):
    """Model ConfiguracaoSistema"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='configuracoes_configuracaosistema',
    #     verbose_name='Empresa'
    # )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='configuracoes_configuracaosistema_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'ConfiguracaoSistema'
        verbose_name_plural = 'ConfiguracaoSistemas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class ParametroEmpresa(models.Model):
    """Model ParametroEmpresa"""
    
    # Relacionamentos
    # empresa = models.ForeignKey(
    #     on_delete=models.CASCADE,
    #     related_name='configuracoes_parametroempresa',
    #     verbose_name='Empresa'
    # )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='configuracoes_parametroempresa_criado',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'ParametroEmpresa'
        verbose_name_plural = 'ParametroEmpresas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class PerfilUsuario(models.Model):
    """Model PerfilUsuario"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='configuracoes_perfilusuario',
        verbose_name='Empresa'
    )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    # criado_por = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='configuracoes_perfilusuario_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'PerfilUsuario'
        verbose_name_plural = 'PerfilUsuarios'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


class PermissaoCustomizada(models.Model):
    """Model PermissaoCustomizada"""
    
    # Relacionamentos
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='configuracoes_permissaocustomizada',
        verbose_name='Empresa'
    )
    
    # Dados básicos
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    
    # Auditoria
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    # criado_por = models.ForeignKey(
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='configuracoes_permissaocustomizada_criado',
    #     verbose_name='Criado por'
    # )
    
    class Meta:
        verbose_name = 'PermissaoCustomizada'
        verbose_name_plural = 'PermissaoCustomizadas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.nome


