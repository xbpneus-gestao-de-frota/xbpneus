from django.db import models
from django.utils import timezone


class Vehicle(models.Model):
    """Veículo da frota"""
    TIPO_CHOICES = [
        ("CAMINHAO", "Caminhão"),
        ("CARRETA", "Carreta"),
        ("BITREM", "Bitrem"),
        ("RODOTREM", "Rodotrem"),
        ("VUC", "VUC"),
        ("OUTRO", "Outro"),
    ]
    
    STATUS_CHOICES = [
        ("ATIVO", "Ativo"),
        ("MANUTENCAO", "Em Manutenção"),
        ("INATIVO", "Inativo"),
        ("VENDIDO", "Vendido"),
    ]
    
    # Arquitetura Matriz-Filiais
    empresa = models.ForeignKey(
        'transportador_empresas.Empresa',
        on_delete=models.PROTECT,
        related_name='veiculos',
        verbose_name="Empresa",
        null=True,
        blank=True,
        help_text="Empresa proprietária do veículo"
    )
    filial = models.ForeignKey(
        'transportador_empresas.Filial',
        on_delete=models.PROTECT,
        related_name='veiculos',
        verbose_name="Filial",
        null=True,
        blank=True,
        help_text="Filial responsável pelo veículo"
    )
    
    placa = models.CharField(max_length=20, unique=True)

    modelo = models.CharField(max_length=100, blank=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    ano_fabricacao = models.IntegerField(blank=True, null=True)
    ano_modelo = models.IntegerField(blank=True, null=True)
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='CAMINHAO')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    
    # Dados operacionais
    km = models.IntegerField(default=0, help_text='Quilometragem atual')
    km_ultima_manutencao = models.IntegerField(default=0)
    km_proxima_manutencao = models.IntegerField(blank=True, null=True)
    
    # Motorista atual (temporário, será substituído por vínculo)
    motorista = models.CharField(max_length=100, blank=True, null=True)
    
    # Dados técnicos
    chassi = models.CharField(max_length=50, blank=True, null=True)
    renavam = models.CharField(max_length=20, blank=True, null=True)
    capacidade_carga = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Capacidade em toneladas')
    
    # Eixos e pneus
    numero_eixos = models.IntegerField(default=3)
    total_posicoes_pneus = models.IntegerField(default=6, help_text='Total de posições para pneus')
    
    # Datas
    data_aquisicao = models.DateField(blank=True, null=True)
    data_venda = models.DateField(blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['placa']

    def __str__(self):
        return f"{self.placa} - {self.modelo}"
    
    def precisa_manutencao(self):
        """Verifica se veículo precisa de manutenção"""
        if self.km_proxima_manutencao:
            return self.km >= self.km_proxima_manutencao
        return False
    
    def km_ate_manutencao(self):
        """Calcula KM restante até próxima manutenção"""
        if self.km_proxima_manutencao:
            return max(0, self.km_proxima_manutencao - self.km)
        return None


class Position(models.Model):
    """Posição de pneu em um veículo"""
    TIPO_EIXO_CHOICES = [
        ('DIANTEIRO', 'Dianteiro'),
        ('TRACAO', 'Tração'),
        ('LIVRE', 'Livre'),
    ]
    
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='posicoes_pneu')
    
    # Identificação da posição
    posicao = models.CharField(max_length=50, help_text='Ex: 1E, 1D, 2E, 2D')
    eixo = models.IntegerField(help_text='Número do eixo')
    tipo_eixo = models.CharField(max_length=20, choices=TIPO_EIXO_CHOICES, default='LIVRE')
    lado = models.CharField(max_length=1, choices=[('E', 'Esquerdo'), ('D', 'Direito')])
    
    # Medida recomendada
    medida = models.CharField(max_length=50, help_text='Medida do pneu recomendada')
    
    # Pneu atual (será vinculado ao pilar de pneus)
    pneu_atual_codigo = models.CharField(max_length=50, blank=True, null=True)
    
    ordem = models.IntegerField(default=0, help_text='Ordem de exibição')
    
    class Meta:
        verbose_name = 'Posição de Pneu'
        verbose_name_plural = 'Posições de Pneus'
        ordering = ['veiculo', 'ordem', 'eixo', 'lado']
        unique_together = ['veiculo', 'posicao']

    def __str__(self):
        return f"{self.veiculo.placa} - {self.posicao}"


class HistoricoKm(models.Model):
    """Histórico de quilometragem do veículo"""
    veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='historico_km')
    
    km_anterior = models.IntegerField()
    km_atual = models.IntegerField()
    km_rodado = models.IntegerField()
    
    data_leitura = models.DateTimeField(default=timezone.now)
    origem = models.CharField(max_length=50, default='MANUAL', help_text='MANUAL, APP, TELEMETRIA')
    
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Histórico de KM'
        verbose_name_plural = 'Históricos de KM'
        ordering = ['-data_leitura']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.km_atual} km"
