from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    """Clientes da transportadora"""
    TIPO_CHOICES = [
        ("PF", "Pessoa Física"),
        ("PJ", "Pessoa Jurídica"),
    ]
    
    STATUS_CHOICES = [
        ("ATIVO", "Ativo"),
        ("INATIVO", "Inativo"),
        ("BLOQUEADO", "Bloqueado"),
    ]
    

    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    
    nome_razao_social = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=200, blank=True, null=True)
    
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    inscricao_municipal = models.CharField(max_length=20, blank=True, null=True)
    
    # Endereço
    cep = models.CharField(max_length=10, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Dados comerciais
    limite_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prazo_pagamento = models.IntegerField(default=30, help_text='Prazo em dias')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome_razao_social']
    
    def __str__(self):
        return f"{self.nome_razao_social} ({self.cpf_cnpj})"


class ContatoCliente(models.Model):
    """Contatos do cliente"""
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contatos')
    
    nome = models.CharField(max_length=200)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    principal = models.BooleanField(default=False)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Contato do Cliente'
        verbose_name_plural = 'Contatos dos Clientes'
        ordering = ['-principal', 'nome']
    
    def __str__(self):
        return f"{self.nome} - {self.cliente.nome_razao_social}"
