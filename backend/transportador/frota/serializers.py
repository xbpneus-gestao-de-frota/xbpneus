from rest_framework import serializers
from .models import Vehicle, Position
import re

class VehicleSerializer(serializers.ModelSerializer):
    """Serializer para veículos com validações de negócio"""
    
    empresa_nome = serializers.CharField(source='empresa.nome', read_only=True)
    filial_nome = serializers.CharField(source='filial.nome', read_only=True)
    filial_codigo = serializers.CharField(source='filial.codigo', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ['criado_em', 'atualizado_em']
    
    def validate_placa(self, value):
        """
        Valida formato da placa (padrão brasileiro)
        Aceita: ABC1234 ou ABC1D23 (Mercosul)
        """
        if not value:
            raise serializers.ValidationError("Placa é obrigatória")
        
        # Remove espaços e converte para maiúsculas
        placa = value.strip().upper().replace('-', '').replace(' ', '')
        
        # Padrão antigo: ABC1234
        padrao_antigo = re.match(r'^[A-Z]{3}[0-9]{4}$', placa)
        # Padrão Mercosul: ABC1D23
        padrao_mercosul = re.match(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$', placa)
        
        if not (padrao_antigo or padrao_mercosul):
            raise serializers.ValidationError(
                "Formato de placa inválido. Use ABC1234 ou ABC1D23 (Mercosul)"
            )
        
        return placa
    
    def validate_ano_fabricacao(self, value):
        """Valida ano de fabricação"""
        if value is not None:
            from datetime import datetime
            ano_atual = datetime.now().year
            
            if value < 1900:
                raise serializers.ValidationError("Ano de fabricação muito antigo")
            
            if value > ano_atual + 1:
                raise serializers.ValidationError(
                    f"Ano de fabricação não pode ser maior que {ano_atual + 1}"
                )
        
        return value
    
    def validate_ano_modelo(self, value):
        """Valida ano do modelo"""
        if value is not None:
            from datetime import datetime
            ano_atual = datetime.now().year
            
            if value < 1900:
                raise serializers.ValidationError("Ano do modelo muito antigo")
            
            if value > ano_atual + 1:
                raise serializers.ValidationError(
                    f"Ano do modelo não pode ser maior que {ano_atual + 1}"
                )
        
        return value
    
    def validate_km(self, value):
        """Valida quilometragem"""
        if value < 0:
            raise serializers.ValidationError("Quilometragem não pode ser negativa")
        
        if value > 10000000:  # 10 milhões de km
            raise serializers.ValidationError("Quilometragem muito alta, verifique o valor")
        
        return value
    
    def validate_km_ultima_manutencao(self, value):
        """Valida KM da última manutenção"""
        if value < 0:
            raise serializers.ValidationError("KM da última manutenção não pode ser negativo")
        
        return value
    
    def validate_capacidade_carga(self, value):
        """Valida capacidade de carga"""
        if value is not None:
            if value <= 0:
                raise serializers.ValidationError("Capacidade de carga deve ser maior que zero")
            
            if value > 100:  # 100 toneladas
                raise serializers.ValidationError("Capacidade de carga muito alta, verifique o valor")
        
        return value
    
    def validate_numero_eixos(self, value):
        """Valida número de eixos"""
        if value < 2:
            raise serializers.ValidationError("Veículo deve ter no mínimo 2 eixos")
        
        if value > 10:
            raise serializers.ValidationError("Número de eixos muito alto, verifique o valor")
        
        return value
    
    def validate_total_posicoes_pneus(self, value):
        """Valida total de posições de pneus"""
        if value < 4:
            raise serializers.ValidationError("Veículo deve ter no mínimo 4 posições de pneus")
        
        if value > 50:
            raise serializers.ValidationError("Número de posições muito alto, verifique o valor")
        
        return value
    
    def validate(self, data):
        """Validações cruzadas"""
        # Valida que KM atual >= KM última manutenção
        km = data.get('km', 0)
        km_ultima_manutencao = data.get('km_ultima_manutencao', 0)
        
        if km < km_ultima_manutencao:
            raise serializers.ValidationError({
                'km': 'KM atual não pode ser menor que KM da última manutenção'
            })
        
        # Valida que ano modelo >= ano fabricação
        ano_fabricacao = data.get('ano_fabricacao')
        ano_modelo = data.get('ano_modelo')
        
        if ano_fabricacao and ano_modelo:
            if ano_modelo < ano_fabricacao:
                raise serializers.ValidationError({
                    'ano_modelo': 'Ano do modelo não pode ser anterior ao ano de fabricação'
                })
        
        # Valida que se tem data de venda, status deve ser VENDIDO
        data_venda = data.get('data_venda')
        status = data.get('status')
        
        if data_venda and status != 'VENDIDO':
            raise serializers.ValidationError({
                'status': 'Status deve ser VENDIDO quando há data de venda'
            })
        
        return data


class PositionSerializer(serializers.ModelSerializer):
    """Serializer para posições de pneus com validações"""
    
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    
    class Meta:
        model = Position
        fields = ["id", "veiculo", "veiculo_placa", "posicao", "eixo", "tipo_eixo", "lado", "medida", "pneu_atual_codigo", "ordem"]
        read_only_fields = ['id']
    
    def validate_eixo(self, value):
        """Valida número do eixo"""
        if value < 1:
            raise serializers.ValidationError("Número do eixo deve ser maior que zero")
        
        if value > 10:
            raise serializers.ValidationError("Número do eixo muito alto")
        
        return value
    
    def validate_posicao(self, value):
        """Valida formato da posição"""
        if not value:
            raise serializers.ValidationError("Posição é obrigatória")
        
        # Formato esperado: 1E, 1D, 2E, 2D, etc.
        if not re.match(r'^\d+[ED]$', value.upper()):
            raise serializers.ValidationError(
                "Formato de posição inválido. Use formato como 1E, 1D, 2E, etc."
            )
        
        return value.upper()
    
    def validate_medida(self, value):
        """Valida formato da medida do pneu"""
        if not value:
            raise serializers.ValidationError("Medida é obrigatória")
        
        # Formato esperado: 295/80R22.5
        if not re.match(r'^\d+/\d+R\d+\.?\d*$', value):
            raise serializers.ValidationError(
                "Formato de medida inválido. Use formato como 295/80R22.5"
            )
        
        return value
    
    def validate(self, data):
        """Validações cruzadas"""
        veiculo = data.get('veiculo')
        posicao = data.get('posicao')
        
        # Verifica se já existe uma posição com o mesmo nome no veículo
        if veiculo and posicao:
            qs = Position.objects.filter(veiculo=veiculo, posicao=posicao)
            
            # Se estamos atualizando, exclui o registro atual da verificação
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise serializers.ValidationError({
                    'posicao': f'Já existe uma posição {posicao} neste veículo'
                })
        
        return data

