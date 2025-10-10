#!/usr/bin/env python3
"""
Script de Importação de Dados dos CSVs para o Sistema XBPneus
"""
import os
import sys
import django
import csv
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backend.transportador.frota.models import Vehicle, Position
from backend.transportador.models import UsuarioTransportador

# Cores
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text.center(80)}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ️  {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

CSV_DIR = "/home/ubuntu/upload/banco de dados"

def importar_catalogo_modelos():
    """Importa catálogo de modelos de veículos"""
    print_header("IMPORTANDO CATÁLOGO DE MODELOS DE VEÍCULOS")
    
    csv_path = os.path.join(CSV_DIR, "catalogo_modelos_v05.csv")
    
    if not os.path.exists(csv_path):
        print_error(f"Arquivo não encontrado: {csv_path}")
        return 0
    
    # Buscar um transportador para associar os veículos
    transportador = UsuarioTransportador.objects.filter(is_superuser=False).first()
    if not transportador:
        print_error("Nenhum transportador encontrado! Crie um transportador primeiro.")
        return 0
    
    print_info(f"Veículos serão associados ao transportador: {transportador.email}")
    
    count = 0
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                # Extrair dados
                categoria = row.get('categoria', '')
                marca = row.get('marca', '')
                familia = row.get('familia_modelo', '')
                variante = row.get('variante', '')
                ano_inicio = int(row.get('ano_inicio', 2020))
                ano_fim = int(row.get('ano_fim', 2025))
                configuracoes = row.get('configuracoes', '')
                observacoes = row.get('observacoes', '')
                
                # Determinar tipo baseado na categoria
                tipo_veiculo = 'CAMINHAO'
                if 'Ônibus' in categoria:
                    tipo_veiculo = 'OUTRO'
                elif 'Carreta' in categoria:
                    tipo_veiculo = 'CARRETA'
                
                # Gerar placa fictícia baseada no índice
                placa_base = f"{marca[:3].upper()}{count:04d}"
                
                # Criar veículo de exemplo
                modelo_nome = f"{marca} {familia} {variante}"
                
                # Verificar se já existe
                if Vehicle.objects.filter(placa=placa_base).exists():
                    continue
                
                vehicle = Vehicle.objects.create(
                    placa=placa_base,
                    modelo=modelo_nome[:100],
                    marca=marca[:50],
                    ano_fabricacao=ano_inicio,
                    ano_modelo=ano_fim,
                    tipo=tipo_veiculo,
                    status='ATIVO',
                    observacoes=f"{observacoes}\nConfig: {configuracoes}"[:500] if observacoes else configuracoes[:500]
                )
                
                count += 1
                if count % 5 == 0:
                    print_info(f"   Importados: {count} veículos...")
                
            except Exception as e:
                print_error(f"Erro ao importar linha: {str(e)}")
                continue
    
    print_success(f"Total de veículos importados: {count}")
    return count

def importar_mapa_posicoes():
    """Importa mapa de posições de pneus"""
    print_header("IMPORTANDO MAPA DE POSIÇÕES DE PNEUS")
    
    csv_path = os.path.join(CSV_DIR, "mapa_posicoes_v05.csv")
    
    if not os.path.exists(csv_path):
        print_error(f"Arquivo não encontrado: {csv_path}")
        return 0
    
    # Pegar alguns veículos para adicionar posições
    veiculos = Vehicle.objects.all()[:10]
    
    if not veiculos:
        print_error("Nenhum veículo encontrado! Importe veículos primeiro.")
        return 0
    
    count = 0
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        posicoes_template = list(reader)
    
    # Aplicar posições aos veículos
    for veiculo in veiculos:
        for idx, row in enumerate(posicoes_template):
            try:
                config_id = row.get('config_id', '')
                componente = row.get('componente', '')
                eixo = int(row.get('eixo', 1))
                lado = row.get('lado', 'L')
                posicao_tipo = row.get('posicao_tipo', '')
                position_id = row.get('position_id', '')
                
                # Converter lado
                lado_map = {'L': 'E', 'R': 'D'}
                lado_convertido = lado_map.get(lado, 'E')
                
                # Determinar tipo de eixo
                tipo_eixo = 'LIVRE'
                if 'direcao' in posicao_tipo.lower():
                    tipo_eixo = 'DIANTEIRO'
                elif 'tracao' in posicao_tipo.lower():
                    tipo_eixo = 'TRACAO'
                
                # Verificar se já existe
                if Position.objects.filter(veiculo=veiculo, posicao=position_id).exists():
                    continue
                
                Position.objects.create(
                    veiculo=veiculo,
                    posicao=position_id,
                    eixo=eixo,
                    tipo_eixo=tipo_eixo,
                    lado=lado_convertido,
                    medida="295/80R22.5",  # Medida padrão
                    ordem=idx
                )
                
                count += 1
                
            except Exception as e:
                print_error(f"Erro ao criar posição: {str(e)}")
                continue
    
    print_success(f"Total de posições criadas: {count}")
    return count

def criar_veiculos_exemplo():
    """Cria veículos de exemplo com dados realistas"""
    print_header("CRIANDO VEÍCULOS DE EXEMPLO")
    
    # Buscar transportador
    transportador = UsuarioTransportador.objects.filter(is_superuser=False).first()
    if not transportador:
        print_error("Nenhum transportador encontrado!")
        return 0
    
    veiculos_exemplo = [
        {
            'placa': 'ABC1234',
            'modelo': 'Scania R450 6x2',
            'marca': 'Scania',
            'ano_fabricacao': 2020,
            'ano_modelo': 2021,
            'tipo': 'CAMINHAO',
            'status': 'ATIVO',
            'km': 150000,
            'numero_eixos': 3,
            'total_posicoes_pneus': 10,
            'motorista': 'João Silva',
            'observacoes': 'Veículo para longa distância'
        },
        {
            'placa': 'DEF5678',
            'modelo': 'Volvo FH 540 6x4',
            'marca': 'Volvo',
            'ano_fabricacao': 2019,
            'ano_modelo': 2020,
            'tipo': 'CAMINHAO',
            'status': 'ATIVO',
            'km': 280000,
            'numero_eixos': 3,
            'total_posicoes_pneus': 10,
            'motorista': 'Maria Santos',
            'observacoes': 'Veículo para carga pesada'
        },
        {
            'placa': 'GHI9012',
            'modelo': 'Mercedes-Benz Actros 2651',
            'marca': 'Mercedes-Benz',
            'ano_fabricacao': 2021,
            'ano_modelo': 2022,
            'tipo': 'CAMINHAO',
            'status': 'ATIVO',
            'km': 95000,
            'numero_eixos': 3,
            'total_posicoes_pneus': 10,
            'motorista': 'Carlos Oliveira',
            'observacoes': 'Veículo novo, baixa quilometragem'
        },
        {
            'placa': 'JKL3456',
            'modelo': 'Volkswagen Constellation 25.460',
            'marca': 'Volkswagen',
            'ano_fabricacao': 2018,
            'ano_modelo': 2019,
            'tipo': 'CAMINHAO',
            'status': 'MANUTENCAO',
            'km': 420000,
            'numero_eixos': 3,
            'total_posicoes_pneus': 10,
            'motorista': None,
            'observacoes': 'Em manutenção preventiva'
        },
        {
            'placa': 'MNO7890',
            'modelo': 'Iveco Stralis 570S',
            'marca': 'Iveco',
            'ano_fabricacao': 2022,
            'ano_modelo': 2023,
            'tipo': 'CAMINHAO',
            'status': 'ATIVO',
            'km': 45000,
            'numero_eixos': 3,
            'total_posicoes_pneus': 10,
            'motorista': 'Pedro Costa',
            'observacoes': 'Veículo recém adquirido'
        }
    ]
    
    count = 0
    for dados in veiculos_exemplo:
        try:
            # Verificar se já existe
            if Vehicle.objects.filter(placa=dados['placa']).exists():
                print_info(f"   Veículo {dados['placa']} já existe, pulando...")
                continue
            
            vehicle = Vehicle.objects.create(**dados)
            print_success(f"   Criado: {vehicle.placa} - {vehicle.modelo}")
            count += 1
            
        except Exception as e:
            print_error(f"Erro ao criar veículo {dados['placa']}: {str(e)}")
            continue
    
    print_success(f"Total de veículos de exemplo criados: {count}")
    return count

def criar_posicoes_padrao():
    """Cria posições padrão de pneus para veículos sem posições"""
    print_header("CRIANDO POSIÇÕES PADRÃO DE PNEUS")
    
    # Configuração padrão 6x2 (3 eixos, 10 pneus)
    posicoes_padrao = [
        # Eixo 1 - Direção (2 pneus)
        {'posicao': '1E', 'eixo': 1, 'tipo_eixo': 'DIANTEIRO', 'lado': 'E', 'medida': '295/80R22.5', 'ordem': 1},
        {'posicao': '1D', 'eixo': 1, 'tipo_eixo': 'DIANTEIRO', 'lado': 'D', 'medida': '295/80R22.5', 'ordem': 2},
        
        # Eixo 2 - Tração (4 pneus)
        {'posicao': '2EE', 'eixo': 2, 'tipo_eixo': 'TRACAO', 'lado': 'E', 'medida': '295/80R22.5', 'ordem': 3},
        {'posicao': '2EI', 'eixo': 2, 'tipo_eixo': 'TRACAO', 'lado': 'E', 'medida': '295/80R22.5', 'ordem': 4},
        {'posicao': '2DE', 'eixo': 2, 'tipo_eixo': 'TRACAO', 'lado': 'D', 'medida': '295/80R22.5', 'ordem': 5},
        {'posicao': '2DI', 'eixo': 2, 'tipo_eixo': 'TRACAO', 'lado': 'D', 'medida': '295/80R22.5', 'ordem': 6},
        
        # Eixo 3 - Livre (4 pneus)
        {'posicao': '3EE', 'eixo': 3, 'tipo_eixo': 'LIVRE', 'lado': 'E', 'medida': '295/80R22.5', 'ordem': 7},
        {'posicao': '3EI', 'eixo': 3, 'tipo_eixo': 'LIVRE', 'lado': 'E', 'medida': '295/80R22.5', 'ordem': 8},
        {'posicao': '3DE', 'eixo': 3, 'tipo_eixo': 'LIVRE', 'lado': 'D', 'medida': '295/80R22.5', 'ordem': 9},
        {'posicao': '3DI', 'eixo': 3, 'tipo_eixo': 'LIVRE', 'lado': 'D', 'medida': '295/80R22.5', 'ordem': 10},
    ]
    
    veiculos = Vehicle.objects.all()
    count = 0
    
    for veiculo in veiculos:
        # Verificar se já tem posições
        if veiculo.posicoes_pneu.exists():
            continue
        
        for pos_data in posicoes_padrao:
            try:
                Position.objects.create(
                    veiculo=veiculo,
                    **pos_data
                )
                count += 1
            except Exception as e:
                print_error(f"Erro ao criar posição {pos_data['posicao']} para {veiculo.placa}: {str(e)}")
                continue
        
        print_info(f"   Posições criadas para: {veiculo.placa}")
    
    print_success(f"Total de posições criadas: {count}")
    return count

def exibir_estatisticas():
    """Exibe estatísticas dos dados importados"""
    print_header("ESTATÍSTICAS DO BANCO DE DADOS")
    
    total_veiculos = Vehicle.objects.count()
    veiculos_ativos = Vehicle.objects.filter(status='ATIVO').count()
    veiculos_manutencao = Vehicle.objects.filter(status='MANUTENCAO').count()
    total_posicoes = Position.objects.count()
    
    print_info(f"Total de veículos: {total_veiculos}")
    print_info(f"  - Ativos: {veiculos_ativos}")
    print_info(f"  - Em manutenção: {veiculos_manutencao}")
    print_info(f"Total de posições de pneus: {total_posicoes}")
    
    if total_veiculos > 0:
        print_info(f"Média de posições por veículo: {total_posicoes / total_veiculos:.1f}")
    
    # Mostrar alguns veículos
    print(f"\n{BLUE}Exemplos de veículos cadastrados:{RESET}")
    for v in Vehicle.objects.all()[:5]:
        print(f"  • {v.placa} - {v.modelo} ({v.status}) - {v.posicoes_pneu.count()} posições")

def main():
    """Função principal"""
    print_header("IMPORTAÇÃO DE DADOS - SISTEMA XBPNEUS")
    print_info(f"Diretório CSV: {CSV_DIR}")
    print_info(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # 1. Criar veículos de exemplo
        criar_veiculos_exemplo()
        
        # 2. Importar catálogo de modelos (mais veículos)
        importar_catalogo_modelos()
        
        # 3. Criar posições padrão
        criar_posicoes_padrao()
        
        # 4. Importar mapa de posições (se houver veículos sem posições)
        importar_mapa_posicoes()
        
        # 5. Exibir estatísticas
        exibir_estatisticas()
        
        print_header("IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
        
    except Exception as e:
        print_error(f"Erro geral: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

