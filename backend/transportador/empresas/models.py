from django.db import models
from django.core.exceptions import ValidationError


class Empresa(models.Model):
    """Empresa (Matriz) - Cliente do sistema SaaS"""
    
    TIPOS = [
        ('transportador', 'Transportador'),
        ('revenda', 'Revenda'),
        ('borracharia', 'Borracharia'),
        ('recapagem', 'Recapagem'),
    ]
    
    # Dados Básicos
    nome = models.CharField(max_length=255, help_text="Nome fantasia")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    cnpj = models.CharField(max_length=20, unique=True)
    
    # Dados Fiscais
    razao_social = models.CharField(max_length=255, blank=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True)
    
    # Endereço da Matriz
    cep = models.CharField(max_length=10, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    pais = models.CharField(max_length=50, default='Brasil')
    
    # Contato
    telefone_principal = models.CharField(max_length=20, blank=True)
    email_principal = models.EmailField(blank=True)
    site = models.URLField(blank=True)
    
    # Configurações
    logo = models.ImageField(upload_to='empresas/logos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    
    def total_filiais(self):
        """Retorna o número de filiais ativas"""
        return self.filiais.filter(ativo=True).count()
    
    def total_veiculos(self):
        """Retorna o total de veículos de todas as filiais"""
        from transportador.frota.models import Vehicle
        return Vehicle.objects.filter(empresa=self).count()


class Filial(models.Model):
    """Filial - Unidade operacional de uma Empresa (Matriz)"""
    
    TIPOS_FILIAL = [
        ('OPERACIONAL', 'Operacional'),
        ('ADMINISTRATIVO', 'Administrativo'),
        ('OFICINA_INTERNA', 'Oficina Interna'),
        ('PONTO_APOIO', 'Ponto de Apoio'),
    ]
    
    # Relacionamento com Matriz
    empresa_matriz = models.ForeignKey(
        'Empresa',
        on_delete=models.CASCADE,
        related_name='filiais',
        help_text="Empresa (Matriz) à qual esta filial pertence"
    )
    
    # Identificação
    codigo = models.CharField(max_length=20, help_text="Código interno da filial (ex: FIL001)")
    nome = models.CharField(max_length=255, help_text="Nome da filial (ex: Filial São Paulo)")
    tipo = models.CharField(max_length=20, choices=TIPOS_FILIAL, default='OPERACIONAL')
    
    # Dados Fiscais (opcional - filial pode ter CNPJ próprio)
    cnpj = models.CharField(max_length=20, blank=True, unique=True, null=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True)
    
    # Endereço
    cep = models.CharField(max_length=10, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    responsavel = models.CharField(max_length=200, blank=True, help_text="Nome do responsável pela filial")
    
    # Configurações
    ativo = models.BooleanField(default=True)
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'
        ordering = ['empresa_matriz', 'codigo']
        unique_together = [['empresa_matriz', 'codigo']]
    
    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.empresa_matriz.nome})"
    
    def clean(self):
        """Validações customizadas"""
        # Se filial tem CNPJ, deve ser diferente da matriz
        if self.cnpj and self.cnpj == self.empresa_matriz.cnpj:
            raise ValidationError("CNPJ da filial não pode ser igual ao da matriz")
    
    def total_veiculos(self):
        """Retorna o total de veículos alocados nesta filial"""
        return self.veiculos.filter(ativo=True).count()
    
    def saldo_estoque_pneus(self):
        """Retorna o saldo de pneus em estoque nesta filial"""
        from transportador.pneus.models import Tire
        return Tire.objects.filter(filial_estoque=self, status='ESTOQUE').count()


class Transportador(models.Model):
    """Cadastro de transportador aguardando aprovação"""
    cnpj = models.CharField(max_length=20, unique=True)
    razao = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    status = models.CharField(
        max_length=20,
        choices=[("PENDENTE", "Pendente"), ("APROVADO", "Aprovado"), ("RECUSADO", "Recusado")],
        default="PENDENTE",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.razao

